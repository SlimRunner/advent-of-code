#include <iostream>
#include <string>
#include <sstream>
#include <fstream>

#include <vector>
#include <map>

#define IO_USE \
  using std::cout; \
  using std::cin; \
  using std::endl; \
  using std::string;

using argmap = std::map<std::string, std::string>;

argmap getArgs(int argc, char const *argv[]) {
  if (argc == 1) {
    return argmap();
  }
  argmap comms;
  bool parsing = false, first = true;
  std::string k, v;
  for (size_t i = 1; i < argc; ++i) {
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

int nthKernelSum(std::vector<int> v, int n) {
  int count = 0;
  int curr = 0, prev = 0;
  bool first = true;
  for (
    auto it = v.begin(), ht = v.begin();
    it != v.end(); ++it
  ) {
    if (first) {
      first = false;
      for (size_t i = 0; i < n; i++) {
        curr += *it;
        if (i < n - 1) ++it;
      }
    } else {
      curr += *it - *ht;
      if (curr > prev) ++count;
      ++ht;
    }
    prev = curr;
  }
  return count;
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
  std::vector<int> nums;
  while (std::getline(infile, line)) {
    std::istringstream iss(line);
    int num;
    if (iss >> num) {
      nums.push_back(num);
    }
  }
  cout << "part 1: " << nthKernelSum(nums, 1) << endl;
  cout << "part 2: " << nthKernelSum(nums, 3) << endl;
  return 0;
}
