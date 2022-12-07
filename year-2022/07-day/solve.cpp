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

class Token {
private:
  std::string _name;

public:
  Token(std::string name);
  ~Token();

  std::string getName() const { return _name; }
  void setName(std::string name) { _name = name; }
  virtual size_t getSize() const = 0;
};

Token::Token(std::string name) {}

Token::~Token() {}

class Dir : public Token {
private:
  std::map<std::string, Token*> _children;

public:
  Dir(std::string name);
  ~Dir();

  void addChildren(Token* child) {
    if (_children.find(child->getName()) == _children.end()) {
      _children.emplace(child->getName(), child);
    }
  }

  bool hasChild(std::string name) const {
    if (_children.size() == 0) return false;
    auto found = _children.find(name);
    return found != _children.end();
  }

  Token* findChild(std::string name) const {
    auto found = _children.find(name);
    if (found != _children.end()) {
      return found->second;
    }
    throw std::runtime_error("Children not found\n");
  }
  
  virtual size_t getSize() const override {
    size_t size;
    for (auto &&f : _children) {
      size += f.second->getSize();
    }
    return size;
  }
};

Dir::Dir(std::string name) : Token(name) {
  _children = {};
}

Dir::~Dir() {}

class File : public Token {
private:
  size_t _size;

public:
  File(std::string name, size_t size);
  ~File();

  virtual size_t getSize() const override { return _size; }
};

File::File(std::string name, size_t size) : Token(name), _size(size) {}

File::~File() {}

int getSizeSum(vecstring input) {
  IO_USE
  string cmd;
  Dir root("/");
  Token* here;
  for (auto &&line : input) {
    if (line.at(0) == '$') {
      cmd = line.substr(2, 2);
      string param = line.substr(4);
      cout << cmd << ": " << param << '\n';
      if (cmd == "cd") {
        if (param == "/") {
          here = &root;
        } else {
          cout << "before dyn cast\n";
          Dir * dere = static_cast<Dir*>(here);
          if (!dere) cout << "cast failed\n";
          if (!dere->hasChild(param)) {
            cout << "after\n";
            Dir* newDir = new Dir(param);
            dere->addChildren(newDir);
          }
        }
      }
    } else {
    }
  }

  cout << '\n';
  return 1;
}

int main(int argc, char const *argv[]) {
  IO_USE;
  argmap params = getArgs(argc, argv);
  vecstring input = getInput(params);
  if (hasKey("-v", params)) {
    printLines(input);
  }

  cout << "part 1: " << getSizeSum(input) << endl;
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
