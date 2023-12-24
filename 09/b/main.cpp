#include <algorithm>
#include <fstream>
#include <iostream>
#include <numeric>
#include <ranges>
#include <sstream>
#include <vector>

int get_prediction(const std::ranges::forward_range auto& v) {
  std::vector<std::ranges::range_value_t<decltype(v)>> diffs(v.size());
  auto first_elts_sum{v.front()};

  std::adjacent_difference(std::begin(v), std::end(v), std::begin(diffs));

  for (
    std::size_t num_diffs{v.size()}, i{};
    !std::all_of(
      std::next(std::cbegin(diffs)),
      std::next(std::cbegin(diffs), num_diffs),
      [](const auto x) { return x == 0; }
    );
    --num_diffs, ++i
  ) {
    first_elts_sum += (i % 2 ? 1 : -1) * *std::next(std::cbegin(diffs));
    std::adjacent_difference(
      std::next(std::begin(diffs)),
      std::next(std::begin(diffs), num_diffs),
      std::begin(diffs)
    );
  }
  return first_elts_sum;
}

int main(const int, const char** argv) {
  std::ifstream input_file_stream{argv[1]};
  std::string line;
  int num, answer{};
  std::vector<std::vector<int>> histories;

  while (std::getline(input_file_stream, line)) {
    histories.emplace_back();
    std::stringstream ss;
    ss << line;
    while (ss >> num) {
      histories.back().push_back(num);
    }
  }

  for (const auto& history: histories) {
    answer += get_prediction(history);
  }

  std::cout << answer << '\n';
}
