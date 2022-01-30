#include <iostream>
#include <string>
#include <sstream>
#include <fstream>

#include <bitset>
#include <vector>
#include <map>

#define IO_USE \
  using std::cout; \
  using std::cin; \
  using std::endl; \
  using std::string;

using intPair = std::pair<int, int>;
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

int pairProduct(intPair p) {
  return p.first * p.second;
}

intPair getRates(std::vector<std::string> bits) {
  std::map<int, int> tally;
  for (auto b = bits.begin(); b != bits.end(); ++b) {
    for (size_t i = 0; i < b->size(); ++i) {
      int d = (*b)[i] == '1' ? 1 : 0;
      auto it = tally.find(i);
      if (it != tally.end()) {
        if (d) it->second++;
      } else {
        tally.insert(std::make_pair(i, d));
      }
    }
  }
  int obits = 0;
  int nh = bits.size() / 2;
  size_t L = tally.size();
  for (size_t i = 0; i < L; ++i) {
    if (tally.at(i) > nh) {
      obits = obits | 1 << (L - i - 1);
    }
  }
  return intPair(obits, obits ^ ((1 << L) - 1));
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
  std::vector<string> bits;
  while (std::getline(infile, line)) {
    if (line.size()) {
      bits.push_back(line);
    }
  }
  cout << "part 1: " << pairProduct(getRates(bits)) << endl;
  // cout << "part 2: " << "" << endl;
  return 0;
}
