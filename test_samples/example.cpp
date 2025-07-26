#include <iostream>
#include <vector>

int findMax(const std::vector<int>& nums) {
    int maxVal = nums[0];
    for (int i = 1; i < nums.size(); ++i) {
        if (nums[i] > maxVal)
            maxVal = nums[i];
    }
    return maxVal;
}

bool isEven(int number) {
    return number % 2 == 0;
}

void printPrimes(int limit) {
    for (int num = 2; num <= limit; ++num) {
        bool isPrime = true;
        for (int i = 2; i * i <= num; ++i) {
            if (num % i == 0) {
                isPrime = false;
                break;
            }
        }
        if (isPrime)
            std::cout << num << " ";
    }
    std::cout << std::endl;
}

int factorial(int n) {
    if (n <= 1)
        return 1;
    return n * factorial(n - 1);
}

int main() {
    std::vector<int> data = {3, 7, 2, 9, 5};
    std::cout << "Max: " << findMax(data) << std::endl;
    printPrimes(20);
    std::cout << "Factorial of 5: " << factorial(5) << std::endl;
    return 0;
}
