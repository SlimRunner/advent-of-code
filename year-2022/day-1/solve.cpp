#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

#include <algorithm>
#include <map>
#include <vector>

#define IO_USE                                                                 \
  using std::cout;                                                             \
  using std::cin;                                                              \
  using std::endl;                                                             \
  using std::string;

using argmap = std::map<std::string, std::string>;

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

bool hasKey(std::string key, argmap args) {
  return args.find(key) != args.end();
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
  std::vector<int> elves;
  elves.push_back(0);
  std::vector<int> largest;

  while (std::getline(infile, line)) {
    std::istringstream iss(line);
    int cal = 0;
    if (line.size()) {
      iss >> cal;
      elves.back() += cal;
    } else {
      elves.push_back(0);
    }
  }

  int top3 = 0;
  std::sort(elves.begin(), elves.end());
  cout << "part 1: " << largest.back() << endl;
  for (size_t i = 0; i < 3; ++i) {
    cout << elves.back() << endl;
    top3 += elves.back();
    elves.pop_back();
  }
  cout << "part 2: " << top3 << endl;
  return 0;
}
