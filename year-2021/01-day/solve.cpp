#include <iostream>
#include <string>
#include <sstream>
#include <fstream>

#include <map>

#define IO_USE \
  using std::cout; \
  using std::cin; \
  using std::endl; \
  using std::string; \

using argmap = std::map<std::string, std::string>;

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
  std::ifstream infile("data.in.txt");
  string line;
  int curr, prev;
  int n = 0;
  bool first = true;
  while (std::getline(infile, line)) {
    std::istringstream iss(line);
    iss >> curr;
    if (!first) {
      n += (curr > prev ? 1 : 0);
    }
    prev = curr;
    first = false;
  }
  cout << "part 1: " << n;
  argmap params = getArgs(argc, argv);
  /* code here */
  return 0;
}
