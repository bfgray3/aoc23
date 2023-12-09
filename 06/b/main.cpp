#include <cmath>
#include <fstream>
#include <iostream>
#include <numeric>
#include <ranges>
#include <regex>
#include <vector>

// TODO: fewer casts

unsigned long get_num_from_line(const std::string& s) {
  std::regex r{R"(\D)"};
  return std::stoul(std::regex_replace(s, r, ""));
}

template <typename T>
std::pair<double, double> get_intercepts(T time, T record) {
  auto time_d{static_cast<double>(time)}, record_d{static_cast<double>(record)};
  auto discriminant{std::sqrt(std::pow(time_d, 2) - 4 * record_d)};
  return {std::ceil((time_d - discriminant) / 2), std::floor((time_d + discriminant) / 2)};
}

int main(const int, const char** argv) {
  unsigned long time{}, distance{};
  std::ifstream input_file_stream{argv[1]};
  std::string line;

  while (std::getline(input_file_stream, line)) {
    if (line.starts_with("Time")) {
      time = get_num_from_line(line);
    } else {
      distance = get_num_from_line(line);
    }
  }

  auto [low, high] = get_intercepts(time, distance);

  // can't tie record, have to beat it
  if (static_cast<unsigned long>((static_cast<double>(time) - low) * low) == distance) {
    ++low;
    --high;
  }

  std::cout << static_cast<unsigned long>(high - low + 1) << '\n';
}
