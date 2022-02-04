#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

#include <map>
#include <vector>

#define IO_USE                                                                 \
  using std::cout;                                                             \
  using std::cin;                                                              \
  using std::endl;                                                             \
  using std::string;

using argmap = std::map<std::string, std::string>;
using coordinate = std::pair<int, int>;
using lineSeg = std::pair<coordinate, coordinate>;

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

lineSeg parseLine(std::string src) {
  std::stringstream ss;
  std::array<int, 4> buff = {0, 0, 0, 0};
  auto bfit = buff.begin();
  bool consuming = true;
  for (auto it = src.begin(); it != src.end() && bfit != buff.end(); ++it) {
    /* WARNING: only works with positive numbers*/
    if (*it >= '0' && *it <= '9') {
      consuming = true;
      ss << *it;
    } else if (consuming && (*it == ' ' || *it == ',')) {
      consuming = false;
      ss >> *(bfit++);
      ss.str(std::string());
      ss.clear();
    }
  }
  if (bfit != buff.end()) {
    ss >> *(bfit);
  }
  coordinate x(buff[0], buff[1]);
  coordinate y(buff[2], buff[3]);
  return lineSeg(x, y);
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
  std::vector<lineSeg> lines;
  while (std::getline(infile, line)) {
    std::istringstream iss(line);
    /* declare variables */
    if (line.size()) {
      lines.push_back(parseLine(iss.str()));
    }
  }
  cout << "part 1: " << 0 << endl;
  // cout << "part 2: " << "" << endl;
  return 0;
}
