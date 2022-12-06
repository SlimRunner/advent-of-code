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
#include <regex>

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

  const int SZ = 4;
  const int LN = (input.front().length() + 1) / 4;
  cout << "SIZE " << SZ << endl;
  cout << "LEN " << LN << endl;
  cout << "\n\n";
  std::vector<vecstring> map(LN);
  bool parseMap = true;
  for (auto &&line : input) {
    if (line.length() == 0 && parseMap) {
      parseMap = false;
      for (auto &s : map) {
        std::reverse(s.begin(), s.end());
      }
      continue;
      cout << "\n\n";
    }
    if (parseMap) {
      for (int i = 0; i < LN; ++i) {
        auto ci = line.at((i + 1) * SZ - 3);
        string si(1, ci);
        if (si != " " && ci > '9') {
          map.at(i).push_back(si);
        }
      }
    } else if (line.length() != 0) {

      // for (auto &&i : map) {
      //   for (auto &&j : i) {
      //     cout << j;
      //   }
      //   cout << '\n';
      // }
      // cout << '\n';
      std::smatch nums;
      std::regex_search(line, nums, std::regex("move (\\d+) from (\\d+) to (\\d+)"));
      int me = std::stoi(nums[1].str());
      int from = std::stoi(nums[2].str()) - 1;
      int to = std::stoi(nums[3].str()) - 1;
      for (size_t i = 0; i < me; ++i) {
        size_t S = map.at(from).size() - me + i;
        // cout << "put " << S << " from column " << from + 1 << " in column " << to + 1 << '\n';
        map.at(to).push_back(map.at(from).at(S));
        map.at(from).erase(map.at(from).begin() + S);
      }
      
    }
  }
  
  std::stringstream p1;
  for (auto &&i : map) {
    p1 << i.back();
  }

  cout << "part 2: " << p1.str() << endl;
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
