#include <iostream>
#include <string>
#include <sstream>
#include <fstream>

#include <vector>
#include <map>

#define IO_USE \
  using std::cout; \
  using std::cin; \
  using std::endl; \
  using std::string; \

using argmap = std::map<std::string, std::string>;

enum class Command { FORWARD, DOWN, UP };

// USE .at() command because [] errors out on const maps
const std::map<std::string, Command> MOVES = {
  {"forward", Command::FORWARD},
  {"down", Command::DOWN},
  {"up", Command::UP}
};

argmap getArgs(int argc, char const *argv[]) {
  if (argc == 1) {
    return argmap();
  }
  argmap comms;
  bool parsing = false, first = true;
  std::string k, v;
  for (size_t i = 1; i < argc; ++i) {
    if (argv[i][0] == '-') {
      if (!first) {
        comms.emplace(k, v);
      }
      first = false;
      k = std::string(argv[i]);
      v = "";
      parsing = true;
    } else if (parsing) {
      v += std::string(argv[i]);
    }
  }
  comms.emplace(k, v);
  return comms;
}

bool haveKey(std::string key, argmap args) {
  return args.find(key) != args.end();
}

int main(int argc, char const *argv[]) {
  IO_USE;
  const argmap params = getArgs(argc, argv);
  std::ifstream infile("data.in.txt");
  string line;
  int depth = 0, pos = 0;
  while (std::getline(infile, line)) {
    std::istringstream iss(line);
    std::string comm;
    int value;
    iss >> comm;
    iss >> value;
    switch (MOVES.at(comm)) {
      case Command::FORWARD:
        pos += value;
        break;
      case Command::DOWN:
        depth += value;
        break;
      case Command::UP:
        depth -= value;
        break;
    }
  }
  cout << "part 1: " << pos * depth << endl;
  return 0;
}
