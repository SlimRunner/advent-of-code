#include <fstream>
#include <iostream>
#include <memory>
#include <sstream>
#include <string>

#include <algorithm>

#include <array>
#include <list>
#include <map>
#include <regex>
#include <set>
#include <tuple>
#include <vector>

#define IO_USE                                                                 \
  using std::cout;                                                             \
  using std::cin;                                                              \
  using std::endl;                                                             \
  using std::string;

using argmap = std::map<std::string, std::string>;
using vecstring = std::vector<std::string>;
using pathmap = std::map<std::string, int>;

void printLines(const vecstring &);
vecstring getInput(const argmap &);
argmap getArgs(int, char const **);
bool hasKey(const std::string &, const argmap &);

enum class Command { CD = 0, LS = 1 };

class Path {
private:
  Path* _parent;
  bool _setPar;
  std::map<std::string, Path*> _children;
  std::map<std::string, int> _files;
  std::string _name;

public:
  Path(std::string name);
  ~Path();

  void setName(std::string name) noexcept { _name = name; }

  std::string getName() noexcept { return _name; }

  // Path(const Path& other) {
  //   *this->_parent = *other._parent;
  //   std::copy(other._children.cbegin(), other._children.cend(), this->_children.begin());
  //   std::copy(other._files.cbegin(), other._files.cend(), this->_files.begin());
  //   this->_name = other._name;
  // }

  // Path& operator = (const Path& rhs) {
  //   *this->_parent = *rhs._parent;
  //   std::copy(rhs._children.cbegin(), rhs._children.cend(), this->_children.begin());
  //   std::copy(rhs._files.cbegin(), rhs._files.cend(), this->_files.begin());
  //   this->_name = rhs._name;
  //   return *this;
  // }

  std::map<std::string, Path*> getChildren() const {
    return _children;
  }

  Path* getParent() {
    if (_setPar) {
      return _parent;
    } else {
      throw std::runtime_error("this path has no parent");
    }
  }

  Path* findChild(std::string m) {
    auto match = _children.find(m);
    if (match != _children.end()) {
      return match->second;
    } else {
      throw std::runtime_error("children queried does not exist");
    }
  }

  void addChild(Path* child) {
    _children.emplace(child->_name, child);
  }

  void addFile(std::string name, int size) {
    _files.emplace(name, size);
  }

};

Path::Path(std::string name) : _name(name), _setPar(false) {}

Path::~Path() {
  _children.clear();
  _files.clear();
}

Path* getSizeSum(vecstring comms) {
  IO_USE
  Path* curr;
  bool parsing = false;
  for (auto &&c : comms) {
    if (c.at(0) == '$') {
      parsing = false;
      const string cm = c.substr(2, 2);
      if (cm == "cd") {
        string fn = c.substr(3);
        if (fn == "/") {
          curr = new Path("/");
        } else if (fn == "..") {
          curr = curr->getParent();
        } else {
          curr = curr->findChild(fn);
        }
      } else if (cm == "ls") {
        parsing = true;
      }
    } else {
      std::smatch matches;
      if (std::regex_search(c, matches, std::regex("^(\\w+) [\\w\\.]+"))) {
        auto mit = ++matches.begin();
        std::string m1 = mit->str(), m2 = (++mit)->str();
        if (m1 == "dir") {
          curr->addChild(new Path(m2));
        } else {
          curr->addFile(m2, std::stoi(m1));
        }
      }
    }
  }
  return curr;
}

int main(int argc, char const *argv[]) {
  IO_USE;
  argmap params = getArgs(argc, argv);
  vecstring input = getInput(params);
  if (hasKey("-v", params)) {
    printLines(input);
  }

  Path paths("/");
  Path * dir = getSizeSum(input); // <- this crashes at runtime
  pathmap map;

  // cout << "part 1: " << getSizeSum() << endl;
  cout << "name of root" << paths.getName();
  cout << "part 2: " << "" << endl;
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
