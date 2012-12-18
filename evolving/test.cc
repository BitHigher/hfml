#include <string>
#include <iostream>
#include <sstream>

using std::string;

int add(int a, int b){
	return a + b;
}

int main(){
	std::ostringstream ss;
	ss << 12;
	std::cout << ss.str() << '\n';
	
	int (*x)(int, int) = add;
	std::cout << x(2, 3) << '\n';

}
