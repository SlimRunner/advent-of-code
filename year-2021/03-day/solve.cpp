#include <fstream>
#include <iostream>
#include <string>

#include <list>
#include <map>
#include <vector>

#define IO_USE                                                                 \
  using std::cout;                                                             \
  using std::cin;                                                              \
  using std::endl;                                                             \
  using std::string;

using intpair = std::pair<int, int>;
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

int pairProduct(intpair p) { return p.first * p.second; }

std::vector<int> getTally(const std::vector<std::string> &bits) {
  std::vector<int> tally(bits.at(0).size());
  for (auto b = bits.begin(); b != bits.end(); ++b) {
    for (size_t i = 0; i < b->size(); ++i) {
      int d = (*b)[i] == '1' ? 1 : 0;
      tally.at(i) += d;
    }
  }
  return tally;
}

intpair getGreekRates(const std::vector<int> &tally, size_t size) {
  int bf = 0;
  int half = size / 2;
  size_t bins = tally.size();
  for (size_t i = 0; i < bins; ++i) {
    if (tally.at(i) >= half) {
      bf |= 1 << (bins - i - 1);
    }
  }
  return intpair(bf, bf ^ ((1 << bins) - 1));
}

intpair getElemRating(const std::vector<std::string> &bits,
                      const std::vector<int> &tally) {
  size_t tsize = tally.size();
  bool splitOne = 2 * tally.at(0) >= static_cast<int>(bits.size());
  char bitMode = splitOne ? '1' : '0'; // mode as in statistics
  std::list<std::string> oxy, co2;
  std::vector<int> tOxy(tsize), tCo2(tsize);
  auto addTally = [](std::string s, std::vector<int> &L,
                     bool subtract = false) {
    for (size_t i = 0; i < s.size(); ++i) {
      if (s.at(i) == '1')
        L.at(i) += subtract ? -1 : 1;
    }
  };
  auto binStr = [](std::string s) {
    int out = 0;
    size_t digs = s.size();
    for (size_t i = 0; i < digs; ++i) {
      if (s.at(i) == '1') {
        out |= 1 << (digs - i - 1);
      }
    }
    return out;
  };

  for (auto it = bits.begin(); it != bits.end(); ++it) {
    if (it->at(0) == bitMode) {
      oxy.push_back(*it);
      addTally(*it, tOxy);
    } else {
      co2.push_back(*it);
      addTally(*it, tCo2);
    }
  }

  for (size_t i = 1; i < tsize && oxy.size() > 1; ++i) {
    splitOne = 2 * tOxy.at(i) >= static_cast<int>(oxy.size());
    bitMode = splitOne ? '1' : '0';
    auto it = oxy.begin(), et = oxy.end();
    while (it != et) {
      if (it->at(i) == bitMode) {
        ++it;
      } else {
        addTally(*it, tOxy, true);
        it = oxy.erase(it);
      }
    }
  }

  for (size_t i = 1; i < tsize && co2.size() > 1; ++i) {
    splitOne = 2 * tCo2.at(i) >= static_cast<int>(co2.size());
    bitMode = splitOne ? '1' : '0';
    auto it = co2.begin(), et = co2.end();
    while (it != et) {
      if (it->at(i) != bitMode) {
        ++it;
      } else {
        addTally(*it, tCo2, true);
        it = co2.erase(it);
      }
    }
  }

  return intpair(binStr(oxy.front()), binStr(co2.front()));
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
  std::vector<int> tally = getTally(bits);
  auto gammaEp = getGreekRates(tally, bits.size());
  auto OxyCo2 = getElemRating(bits, tally);
  if (hasKey("-v", params)) {
    cout << std::endl << "RATES" << std::endl;
    cout << "  gamma: " << gammaEp.first;
    cout << " | epsilon: " << gammaEp.second << std::endl;
    cout << "RATINGS" << std::endl;
    cout << "  oxy-gen: " << OxyCo2.first;
    cout << " | co2 scrub: " << OxyCo2.second << std::endl << std::endl;
  }
  cout << "part 1: " << pairProduct(gammaEp) << endl;
  cout << "part 2: " << pairProduct(OxyCo2) << endl;
  return 0;
}
