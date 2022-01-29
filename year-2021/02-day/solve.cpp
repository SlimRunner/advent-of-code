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

enum class Command { FORWARD, DOWN, UP };
using intPair = std::pair<int, int>;
using comPairs = std::vector<std::pair<std::string, int>>;
using argmap = std::map<std::string, std::string>;

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

bool hasKey(std::string key, argmap args) {
  return args.find(key) != args.end();
}

intPair getNaivePiloting(comPairs P) {
  int s = 0, d = 0;
  for (auto p = P.begin(); p != P.end(); ++p) {
    switch (MOVES.at(p->first)) {
      case Command::FORWARD:
        s += p->second;
        break;
      case Command::DOWN:
        d += p->second;
        break;
      case Command::UP:
        d -= p->second;
        break;
    }
  }
  return intPair(s, d);
}

intPair getExpertPiloting(comPairs P) {
  int s = 0, d = 0, a = 0;
  for (auto p = P.begin(); p != P.end(); ++p) {
    switch (MOVES.at(p->first)) {
      case Command::FORWARD:
        s += p->second;
        d += a * p->second;
        break;
      case Command::DOWN:
        a += p->second;
        break;
      case Command::UP:
        a -= p->second;
        break;
    }
  }
  return intPair(s, d);
}

int pairProduct(intPair p) {
  return p.first * p.second;
}

int main(int argc, char const *argv[]) {
  IO_USE;
  const argmap params = getArgs(argc, argv);
  std::string filename = "data.in.txt";
  if (hasKey("-f", params)) {
    filename = params.at("-f");
  };
  std::ifstream infile(filename);
  string line;
  comPairs comms;
  while (std::getline(infile, line)) {
    std::istringstream iss(line);
    std::string comm;
    int value;
    iss >> comm >> value;
    comms.push_back(std::make_pair(comm, value));
  }
  cout << "part 1: " << pairProduct(getNaivePiloting(comms)) << endl;
  cout << "part 2: " << pairProduct(getExpertPiloting(comms)) << endl;
  return 0;
}
