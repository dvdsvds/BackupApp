#pragma once
#include <iostream>
#include <filesystem>
#include <time.h>
#include <chrono>
#include <thread>
#include <mutex>

namespace fs = std::filesystem;

enum class Format {
    ZIP, 
    RAR,
    SEVENZ,
    TAR,
};

enum class Mode {
    Default,
    New
};

enum class Cycle {
    Hourly,
    Daily,
    Weekly,
    Monthly,
    Yearly
};

struct Config {
    fs::path src;
    fs::path dst;
    Format format;
    tm t;

    Mode mode = Mode::Default;
    std::string newName;
    bool include_date = true;

    int cycle_value;
    Cycle cycle;
};

Config parser(int argc, char* argv[]);
bool validate_paths(const Config& path);
fs::path make_backup_name(const Config& cfg);
bool backup(const Config& cfg);

std::chrono::system_clock::time_point cal_cycle(const Config& cfg);
void backup_cycle(const Config& cfg);
void log_message(const std::string& msg);