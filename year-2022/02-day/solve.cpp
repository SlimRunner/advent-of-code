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
using intpair = std::map<int, int>;

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
  std::stringstream c;
  string line;
  int score = 0;
  int score2 = 0;

  while (std::getline(infile, line)) {
    std::istringstream iss(line);
    int a, b;
    a = (int(line[0]) - 65);
    b = (int(line[2]) - 88);
    const int arr[3] = {0,3,6};
    const int arr2[3] = {2,0,1};
    /*
    A, X: rock, draw   -> 1
    B, Y: paper, lose  -> 2
    C, Z: scissor, win -> 3

    001 | 010 -> 3
    010 | 100 -> 6
    100 | 001 -> 
    */
    score += (b + 1) + (a == b ? 3 : 0) + (((a + 1) % 3) == b ? 6 : 0);
    score2 += (((a + arr2[b]) % 3) + 1) + arr[b];
  }
  cout << "part 1: " << score << endl;
  cout << "part 2: " << score2 << endl;

  cout << "\n\nsuccessful run";
  return 0;
}
