#include <fstream>
#include <iostream>
#include <regex>
#include <string>

int main(int argc, char *argv[]) {
  if (argc < 2)
    return 1;

  std::ifstream file(argv[1]);
  if (!file)
    return 2;

  std::string line;
  int functionCount = 0;
  int loopCount = 0;
  int branchCount = 0;

  std::regex funcRegex(R"((\w+\s+)?\w+\s*\([^)]*\)\s*\{)");
  std::regex loopRegex(R"(\b(for|while)\b)");
  std::regex ifRegex(R"(\bif\b)");

  while (std::getline(file, line)) {
    if (std::regex_search(line, funcRegex))
      functionCount++;
    if (std::regex_search(line, loopRegex))
      loopCount++;
    if (std::regex_search(line, ifRegex))
      branchCount++;
  }

  std::cout << "{"
            << "\"functions\": " << functionCount << ", "
            << "\"loops\": " << loopCount << ", "
            << "\"branches\": " << branchCount << "}" << std::endl;
  return 0;
}
