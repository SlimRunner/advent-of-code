#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

#include <algorithm>

#include <array>
#include <list>
#include <map>
#include <tuple>
#include <vector>

#define IO_USE                                                                 \
  using std::cout;                                                             \
  using std::cin;                                                              \
  using std::endl;                                                             \
  using std::string;

using argmap = std::map<std::string, std::string>;
using vecstring = std::vector<std::string>;

void printLines(const vecstring &);
vecstring getInput(const argmap &);
argmap getArgs(int, char const **);
bool hasKey(const std::string &, const argmap &);

int main(int argc, char const *argv[]) {
  IO_USE;
  argmap params = getArgs(argc, argv);
  vecstring input = getInput(params);
  if (hasKey("-v", params)) {
    printLines(input);
  }
  string buff;
  int nexit = 0;

  for (auto &&i : input.front()) {
    ++nexit;
    if (buff.length() < 14) {
      buff.push_back(i);
    } else {
      buff.push_back(i);
      buff.erase(buff.begin());
      bool uq = true; // unique quartet
      for (size_t i = 0; i < buff.length(); ++i) {
        for (size_t j = i + 1; j < buff.length(); ++j) {
          // cout << buff.at(i) << " " << buff.at(j) << '\n';
          uq = uq && buff.at(i) != buff.at(j);
        }
      }
      if (uq) {
        break;
      }
    }
  }
  
  cout << "part 1: " << nexit << endl;
  // cout << "part 2: " << "" << endl;
  return 0;
}

void printLines(const vecstring &input) {
  std::cout << "=================== INPUT START ===================\n";
  for (auto &&i : input) {
    std::cout << i << "\n";
  }
  std::cout << "==================== INPUT END ====================\n";
}

vecstring getInput(const argmap &params) {
  std::string filename = "data.in.txt";
  if (hasKey("-f", params)) {
    filename = params.at("-f");
  } else if (hasKey("-ex", params)) {
    filename = "data.ex.txt";
  }
  std::ifstream infile(filename);
  std::string line;
  vecstring output;

  while (std::getline(infile, line)) {
    output.push_back(line);
  }

  return output;
}

argmap getArgs(int argc, char const *argv[]) {
  if (argc == 1) {
    return argmap();
  }
  argmap comms;
  bool parsing = false, first = true;
  std::string k, v;
  for (int i = 1; i < argc; ++i) {
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

bool hasKey(const std::string &key, const argmap &args) {
  return args.find(key) != args.end();
}
