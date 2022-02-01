#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

#include <algorithm>
#include <map>
#include <tuple>
#include <vector>

#define IO_USE                                                                 \
  using std::cout;                                                             \
  using std::cin;                                                              \
  using std::endl;                                                             \
  using std::string;

using argmap = std::map<std::string, std::string>;
using maprix = std::map<int, std::pair<size_t, size_t>>;
using matrix = std::vector<std::vector<int>>;
using bitrix = std::vector<std::vector<bool>>;
using intpair = std::pair<int, int>;

enum class aisle { ROW, COL };

template <size_t X, size_t Y> class Board {
private:
  maprix _map;
  matrix _mtx;
  bitrix _btx;
  bool _win = false;
  int _wnum;
  std::pair<aisle, int> _wcell;

  bool winyet(int wn) {
    if (_win) {
      return _win;
    }
    auto isTrue = [](bool b) { return b; };
    for (size_t y = 0; y < Y; ++y) {
      auto row = _btx[y];
      // when bingo row found
      if (std::all_of(row.begin(), row.end(), isTrue)) {
        _win = true;
        _wnum = wn;
        _wcell = std::make_pair(aisle::ROW, y);
        return true;
      }
    }
    for (size_t col = 0; col < X; ++col) {
      bool bingo = true;
      for (size_t row = 0; row < Y; ++row) {
        bingo = bingo && _btx[row][col];
      }
      if (bingo) {
        _win = true;
        _wnum = wn;
        _wcell = std::make_pair(aisle::COL, col);
        return true;
      }
    }
    return false;
  }

public:
  Board() {
    _mtx = matrix(Y);
    _btx = bitrix(Y);
    for (size_t i = 0; i < _mtx.size(); ++i) {
      _mtx[i] = std::vector<int>(X);
      _btx[i] = std::vector<bool>(X);
    }
  }

  intpair winLine() {
    if (_win) {
      // switch (_wcell.first) {
      // case aisle::ROW:
      //   return std::make_pair(_wnum, std::vector<int>(_mtx[_wcell.second]));
      //   break;
      // case aisle::COL:
      //   std::vector<int> wc(Y);
      //   for (size_t y = 0; y < Y; y++) {
      //     wc[y] = _mtx[y][_wcell.second];
      //   }
      //   return std::make_pair(_wnum, wc);
      //   break;
      // }
      std::vector<int> wc;
      int usum = 0;
      for (size_t y = 0; y < Y; ++y) {
        for (size_t x = 0; x < X; ++x) {
          if (!_btx[y][x]) {
            usum += _mtx[y][x];
          }
        }
      }
      return std::make_pair(_wnum, usum);
    }
    return std::make_pair(0, 0);
  }

  bool readWin() { return _win; }

  void setCell(size_t x, size_t y, int num) {
    if (x < 0 || x >= X || y < 0 || y >= Y) {
      throw std::out_of_range("Member access is out of range.");
    }
    _mtx[y][x] = num;
    _map.insert(std::make_pair(num, std::make_pair(x, y)));
  }

  bool markNumber(int num) {
    auto fit = _map.find(num);
    if (fit != _map.end()) {
      int x, y;
      std::tie(x, y) = fit->second;
      _btx[y][x].flip();
      return winyet(num);
    }
    return _win;
  }

  bool markCell(size_t x, size_t y) {
    if (x < 0 || x >= X || y < 0 || y >= Y) {
      throw std::out_of_range("Member access is out of range.");
    }
    if (_btx.at(y).at(x)) {
      throw std::invalid_argument(
          "This cell is already marked. Cannot mark twice.");
    }
    _btx[y][x].flip();
    return winyet(_mtx[y][x]);
  }

  int getCell(size_t x, size_t y) {
    if (x < 0 || x >= X || y < 0 || y >= Y) {
      throw std::out_of_range("Member access is out of range.");
    }
    return _mtx[y][x];
  }

  bool getMark(size_t x, size_t y) {
    if (x < 0 || x >= X || y < 0 || y >= Y) {
      throw std::out_of_range("Member access is out of range.");
    }
    return _btx[y][x];
  }

  void print() {
    for (size_t row = 0; row < Y; ++row) {
      for (size_t col = 0; col < X; ++col) {
        std::stringstream ss;
        ss << _mtx[row][col] << (_btx[row][col] ? "+" : " ");
        std::cout << std::setw(4);
        std::cout << ss.str();
      }
      std::cout << std::endl;
    }
    std::cout << std::endl;
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

int pairProduct(intpair p) { return p.first * p.second; }

std::vector<int> parseCSV(std::string csv, const char &sep) {
  // Warning: this function may break with spaces
  std::stringstream ss;
  std::vector<int> out;
  for (auto it = csv.begin(); it != csv.end(); ++it) {
    if (*it == sep) {
      int flush;
      ss >> flush;
      ss.str(std::string());
      ss.clear();
      out.push_back(flush);
    } else {
      ss << *it;
    }
  }
  return out;
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
  std::getline(infile, line);
  std::vector<int> calls = parseCSV(line, ',');
  std::vector<Board<5, 5>> boards;
  std::getline(infile, line); // ignore next empty line
  bool consuming = false;
  int y = 0;
  while (std::getline(infile, line)) {
    std::istringstream iss(line);
    if (line.size()) {
      if (!consuming) {
        boards.push_back(*(new Board<5, 5>));
      }
      int num, x = 0;
      while (iss >> num) {
        boards.back().setCell(x, y, num);
        ++x;
      }
      ++y;
      consuming = true;
    } else {
      if (consuming) {
        y = 0;
      }
      consuming = false;
    }
  }
  bool hasWon = false;
  std::array<intpair, 2> winSel;
  for (auto c = calls.begin(); c != calls.end(); ++c) {
    for (auto b = boards.begin(); b != boards.end(); ++b) {
      if (!b->readWin() && b->markNumber(*c)) {
        winSel.at(hasWon ? 1 : 0) = b->winLine();
        hasWon = true;
      }
    }
  }
  cout << "part 1: " << pairProduct(winSel[0]) << endl;
  cout << "part 2: " << pairProduct(winSel[1]) << endl;
  return 0;
}
