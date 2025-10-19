#include "backend.hpp"
#include <algorithm>
#include <atomic>
#include <fstream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include <pybind11/stl/filesystem.h>

namespace py = pybind11;

Config parser(int argc, char* argv[]) {
    Config cfg;

    for(int i = 1; i < argc; i++) {
        std::string arg = argv[i];

        if(arg == "-s") { // src
            cfg.src = argv[++i];            
        } else if(arg == "-d") { // dist
            cfg.dst = argv[++i];            
        } else if(arg == "-f") { // format
            std::string fmt = argv[++i];
            std::transform(fmt.begin(), fmt.end(), fmt.begin(), [](unsigned char c) {return std::tolower(c); });

            if(fmt == "zip") cfg.format = Format::ZIP;
            else {
                std::cerr << "[Error] Unknown format : " << fmt << std::endl;
                cfg.format = Format::ZIP;
            }
        } else if(arg == "-c") { // cycle
            std::string date = argv[++i];
            std::string temp;
            int parts[3] = {0};
            int idx = 0;

            for(char c : date) {
                if(c == ',' && idx < 3) {
                    parts[idx++] = std::stoi(temp);
                    temp.clear();
                } else {
                    temp += c;
                }
            }

            if(!temp.empty() && idx < 3) {
                parts[idx++] = std::stoi(temp);
            }

            cfg.t.tm_year = parts[0] - 1900;
            cfg.t.tm_mon  = parts[1] - 1;
            cfg.t.tm_mday = parts[2];
            
        } else {
            continue;
        }
    }
    return cfg;
}

bool validate_paths(const Config& cfg) {
    const fs::path& src = cfg.src;
    const fs::path& dst = cfg.dst;


    if (fs::exists(src) && fs::exists(dst)) {
        return true;
    } 
    else if (fs::exists(src) && !fs::exists(dst)) {
        std::cerr << dst << " does not exist." << std::endl;
        std::cout << "Do you want to create new path (dst)? [yes/no] ";

        std::string answer;
        std::getline(std::cin, answer);

        if (!answer.empty() && (answer == "yes" || answer == "y")) {
            std::string dst_name;
            std::cout << "Enter dst name: ";
            std::getline(std::cin, dst_name);

            if (dst_name.empty()) {
                std::cout << "Skipped directory creation (empty input)." << std::endl;
            } else {
                fs::path new_dst = dst / dst_name;
                try {
                    fs::create_directories(new_dst);
                    std::cout << "Created new directory: " << new_dst << std::endl;
                    return true;
                } catch (const fs::filesystem_error& e) {
                    std::cerr << "Failed to create directory: " << e.what() << std::endl;
                }
            }
        } else {
            std::cout << "Skipped directory creation." << std::endl;
        }
    } 
    else if (!fs::exists(src) && fs::exists(dst)) {
        std::cerr << src << " does not exist." << std::endl;
    } 
    else {
        std::cerr << src << ", " << dst << " do not exist." << std::endl;
    }
    return false;
}

fs::path make_backup_name(const Config& cfg) {
    tm t_used = cfg.t;
    if (t_used.tm_year == 0 && t_used.tm_mon == 0 && t_used.tm_mday == 0) {
        auto now = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
        t_used = *std::localtime(&now);
    }

    char buffer[32];
    std::strftime(buffer, sizeof(buffer), "%Y-%m-%d", &t_used);
    std::string date_str = buffer;

    std::string filename = !cfg.newName.empty()
                           ? cfg.newName
                           : cfg.src.filename().string();

    if (cfg.include_date) filename += "_" + date_str;

    return cfg.dst / filename;
}


bool backup(const Config& cfg) {
    try { 
        fs::path backup_path = make_backup_name(cfg);
        std::string src_path = cfg.src.string();
        std::string cmd;

        switch (cfg.format)
        {
            case Format::ZIP:
                cmd = "zip -r \"" + backup_path.string() + ".zip\" \"" + src_path + "\"";
                break;

            case Format::RAR:
                cmd = "rar a \"" + backup_path.string() + ".rar\" \"" + src_path + "\"";
                break;

            case Format::SEVENZ:
                cmd = "7z a \"" + backup_path.string() + ".7z\" \"" + src_path + "\"";
                break;
        }

        int result = std::system(cmd.c_str());
        return result == 0;
    } catch (const std::exception& e) {
        std::cerr << "[Error] Exception in backup(): " << e.what() << std::endl;
        return false;
    }
}


std::chrono::system_clock::time_point cal_cycle(const Config& cfg) {
    auto now = std::chrono::system_clock::now();
    tm next_t = cfg.t;
    auto next_time_t = std::mktime(&next_t);
    next_t = *std::localtime(&next_time_t);

    switch (cfg.cycle)
    {
        case Cycle::Hourly:
            next_t.tm_hour += cfg.cycle_value;
            break;
        case Cycle::Daily:
            next_t.tm_mday += cfg.cycle_value;
            break;
        case Cycle::Weekly:
            next_t.tm_yday += (7 * cfg.cycle_value);
            break;
        case Cycle::Monthly:
            next_t.tm_mon += cfg.cycle_value; 
            break;
        case Cycle::Yearly:
            next_t.tm_year += cfg.cycle_value; 
            break;
    }
    auto next_time = std::mktime(&next_t);
    return std::chrono::system_clock::from_time_t(next_time);
}

std::atomic<bool> running = true;

void backup_cycle(const Config& cfg) {
    int cycle_count = 0;
    auto next_t = cal_cycle(cfg);

    while(running) {
        auto now = std::chrono::system_clock::now();

        if(now >= next_t) {
            ++cycle_count;
            bool result = backup(cfg);

            if (result) 
                log_message("Backup done (" + std::to_string(cycle_count) + ")");
            else 
                log_message("Backup failed (" + std::to_string(cycle_count) + ")");

            next_t = cal_cycle(cfg);
        }

        std::this_thread::sleep_for(std::chrono::seconds(10));
    }
}


std::mutex log_mutex;

void log_message(const std::string& msg) {
    std::lock_guard<std::mutex> lock(log_mutex);
    std::ofstream log("backup.log", std::ios::app);
    auto now_time = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
    log << "[" << std::put_time(std::localtime(&now_time), "%F %T") << "] " << msg << "\n";
}

Config parser_py(const std::vector<std::string>& args) {
    std::vector<char*> argv;
    argv.reserve(args.size());
    for (auto& s : args)
        argv.push_back(const_cast<char*>(s.c_str()));

    return parser(static_cast<int>(args.size()), argv.data());
}

PYBIND11_MODULE(backend, m) {
    m.doc() = "C++ backend module for BackupTool";

    m.def("parser", &parser_py, "Parse command line arguments (Python list)");
    m.def("validate_paths", &validate_paths, "Validate source and destination paths");
    m.def("backup", &backup, "Execute a backup operation");
    m.def("backup_cycle", &backup_cycle, "Run backup in cycle mode");
    m.def("log_message", &log_message, "Write log message to file");

    py::class_<Config>(m, "Config")
        .def(py::init<>())
        .def_readwrite("src", &Config::src)
        .def_readwrite("dst", &Config::dst)
        .def_readwrite("include_date", &Config::include_date)
        .def_readwrite("newName", &Config::newName)
        .def_readwrite("cycle_value", &Config::cycle_value)
        .def_readwrite("t", &Config::t)
        .def_readwrite("format", &Config::format)
        .def_readwrite("mode", &Config::mode)
        .def_readwrite("cycle", &Config::cycle);

    py::enum_<Format>(m, "Format")
        .value("ZIP", Format::ZIP)
        .value("RAR", Format::RAR)
        .value("SEVENZ", Format::SEVENZ)
        .export_values();

    py::enum_<Cycle>(m, "Cycle")
        .value("Hourly", Cycle::Hourly)
        .value("Daily", Cycle::Daily)
        .value("Weekly", Cycle::Weekly)
        .value("Monthly", Cycle::Monthly)
        .value("Yearly", Cycle::Yearly)
        .export_values();

    py::enum_<Mode>(m, "Mode")
        .value("Default", Mode::Default)
        .export_values();
}
