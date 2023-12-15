#include <algorithm>
#include <fstream>
#include <iostream>
#include <regex>
#include <string>
#include <unordered_map>

using LeftRight = std::pair<std::string, std::string>;

int main(const int, const char** argv) {
  std::unordered_map<std::string, LeftRight> nodes;
  std::ifstream input_file_stream{argv[1]};
  std::string line, instructions;
  std::regex r{R"(([0-9A-Z]+) = \(([0-9A-Z]+), ([0-9A-Z]+)\))"};
  std::string current{"AAA"};
  std::smatch match;

  while (std::getline(input_file_stream, line)) {
    if (line.empty()) {
      continue;
    } else if (line.contains('=')) {
      regex_search(line, match, r);
      nodes[match.str(1)] = std::make_pair(match.str(2), match.str(3));
    } else {
      instructions = line;
    }
  }
  unsigned long long i{};
  for (; ; ++i) {
    if (current == "ZZZ") {
      break;
    }
    current = instructions[i % instructions.size()] == 'L' ? nodes.at(current).first : nodes.at(current).second;
  }

  std::cout << i << '\n';
}
