#include <cmath>
#include <fstream>
#include <iostream>
#include <numeric>
#include <ranges>
#include <regex>
#include <vector>

// TODO: fewer casts

unsigned long get_num_from_line(const std::string& s) {
  std::regex r{"[0-9]+"};
  std::stringstream ss;
  for (std::sregex_iterator it{std::sregex_iterator(std::cbegin(s), std::cend(s), r)}; it != std::sregex_iterator(); ++it) {
    ss << it->str();
  }
  return std::stoul(ss.str());
}

template <typename T>
std::pair<double, double> get_intercepts(T time, T record) {
  auto discriminant{std::sqrt(std::pow(static_cast<double>(time), 2) - 4 * static_cast<double>(record))};
  return {std::ceil((static_cast<double>(time) - discriminant) / 2), std::floor((static_cast<double>(time) + discriminant) / 2)};
}

int main(const int, const char** argv) {
  std::vector<unsigned long> ways_to_win;
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

  ways_to_win.push_back(static_cast<unsigned long>(high - low + 1));
  std::cout << static_cast<unsigned long>(high - low + 1) << '\n';
}
