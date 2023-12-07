#include <cmath>
#include <fstream>
#include <iostream>
#include <numeric>
#include <ranges>
#include <regex>
#include <vector>

// TODO: fewer casts

std::vector<unsigned long> get_nums_from_line(const std::string& s) {
  std::regex r{"[0-9]+"};
  std::vector<unsigned long> v;
  for (std::sregex_iterator it{std::sregex_iterator(std::cbegin(s), std::cend(s), r)}; it != std::sregex_iterator(); ++it) {
    v.push_back(std::stoul(it->str()));
  }
  return v;
}

template <typename T>
std::pair<double, double> get_intercepts(T time, T record) {
  auto discriminant{std::sqrt(std::pow(static_cast<double>(time), 2) - 4 * static_cast<double>(record))};
  return {std::ceil((static_cast<double>(time) - discriminant) / 2), std::floor((static_cast<double>(time) + discriminant) / 2)};
}

int main(const int, const char** argv) {
  std::vector<unsigned long> time_vec, distance_vec, ways_to_win;
  std::ifstream input_file_stream{argv[1]};
  std::string line;

  while (std::getline(input_file_stream, line)) {
    if (line.starts_with("Time")) {
      time_vec = get_nums_from_line(line);
    } else {
      distance_vec = get_nums_from_line(line);
    }
  }

  for (const auto& [time, distance]: std::ranges::views::zip(time_vec, distance_vec)) {
    auto [low, high] = get_intercepts(time, distance);

    // can't tie record, have to beat it
    if (static_cast<unsigned long>((static_cast<double>(time) - low) * low) == distance) {
      ++low;
      --high;
    }

    ways_to_win.push_back(static_cast<unsigned long>(high - low + 1));
  }
  std::cout << std::accumulate(std::cbegin(ways_to_win), std::cend(ways_to_win), 1ull, std::multiplies<>()) << '\n';
}
