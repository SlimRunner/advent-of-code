#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

#include <algorithm>
#include <chrono>
#include <map>
#include <unordered_map>
#include <vector>

#define IO_USE                                                                 \
  using std::cout;                                                             \
  using std::cin;                                                              \
  using std::endl;                                                             \
  using std::string;

class coord_hash; // forward declaration
using argmap = std::map<std::string, std::string>;
using coordinate = std::pair<int, int>;
using coordmap = std::unordered_map<coordinate, int>;
using lineSeg = std::pair<coordinate, coordinate>;

template <> class std::hash<coordinate> {
public:
  std::size_t operator()(const coordinate &k) const {
    return std::hash<int>()(k.first) ^ std::hash<int>()(k.second);
  }
};

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

int countOverlaps(std::vector<lineSeg> lines) {
  coordmap field;
  field.reserve(0x8000);
  field.max_load_factor(0.3);
  int overlaps = 0;
  for (auto line = lines.begin(); line != lines.end(); ++line) {
    int x1, y1, x2, y2;
    std::tie(x1, y1) = line->first;
    std::tie(x2, y2) = line->second;
    if (x1 > x2) {
      std::swap(x1, x2);
    }
    if (y1 > y2) {
      std::swap(y1, y2);
    }
    if (x1 == x2) {
      for (int y = y1; y <= y2; ++y) {
        coordinate here(x1, y);
        auto fit = field.find(here);
        if (fit == field.end()) {
          field.insert(std::make_pair(here, 1));
        } else {
          ++(fit->second);
          overlaps += fit->second == 2 ? 1 : 0;
        }
      }
    } else if (y1 == y2) {
      for (int x = x1; x <= x2; ++x) {
        coordinate here(x, y1);
        auto fit = field.find(here);
        if (fit == field.end()) {
          field.insert(std::make_pair(here, 1));
        } else {
          ++(fit->second);
          overlaps += fit->second == 2 ? 1 : 0;
        }
      }
    }
  }
  std::cout << field.bucket_count() << std::endl;
  return overlaps;
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
    if (line.size()) {
      lines.push_back(parseLine(iss.str()));
    }
  }
  std::vector<lineSeg> horzLines;
  auto filterFunc = [](lineSeg line) {
    coordinate a, b;
    std::tie(a, b) = line;
    return a.first == b.first && a.second == b.second;
  };
  std::copy_if(lines.begin(), lines.end(), std::back_inserter(horzLines),
               filterFunc);
  /* ds */
  auto A = std::chrono::high_resolution_clock::now();
  countOverlaps(lines);
  auto B = std::chrono::high_resolution_clock::now();
  cout << std::chrono::duration_cast<std::chrono::microseconds>(B - A).count()
       << endl;
  // cout << "part 1: " << countOverlaps(lines) << endl;
  // cout << "part 2: " << "" << endl;
  return 0;
}
