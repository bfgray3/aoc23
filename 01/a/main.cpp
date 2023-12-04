#include <algorithm>
#include <iostream>
#include <iterator>
#include <numeric>
#include <string>
#include <vector>

#include "utils.h"

int main(const int, const char** argv) {
  // don't need the whole thing in memory at once, but read it all
  // so we can use algorithms
  auto document{utils::read_vector_from_file<std::string>(argv[1])};
  std::vector<char> first, last;

  std::transform(
    std::cbegin(document),
    std::cend(document),
    std::back_inserter(first),
    [](const std::string& s) { return *std::find_if(std::cbegin(s), std::cend(s), ::isdigit); }
  );

  std::transform(
    std::cbegin(document),
    std::cend(document),
    std::back_inserter(last),
    [](const std::string& s) { return *std::find_if(std::crbegin(s), std::crend(s), ::isdigit); }
  );

  auto answer{std::transform_reduce(
    std::cbegin(first),
    std::cend(first),
    std::cbegin(last),
    0ull,
    std::plus<>(),
    [](const char a, const char b) { return 10 * (a - '0') + b - '0'; }
  )};

  std::cout << answer << '\n';
}
