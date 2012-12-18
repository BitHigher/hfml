/*
 * Author: ZhuHanfeng
 * Desc: genetic programming
 */

#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <time.h>
#include <stdlib.h>

using std::string;
using std::vector;

typedef float (*Func)(vector<float> &);

class node{
public:
	virtual float evaluate(vector<float> &input) = 0;
	virtual string name() = 0;
	virtual void display(int indent = 0) = 0;
};

class constnode: public node{
public:
	constnode(float value){
		this->_value = value;
	}

	float evaluate(vector<float> &input){
		return this->_value;
	}

	string name(){
		std::ostringstream ss;
		ss << this->_value;
		return ss.str();
	}

	void display(int indent = 0){
		for(int i = 0; i < indent; ++i)
			std::cout << ' ';
		std::cout << name() << '\n';
	}

private:
	float _value;
};

class paramnode: public node{
public:
	paramnode(int index){
		this->_index = index;
	}

	float evaluate(vector<float> &input){
		return input[this->_index];
	}

	string name(){
		std::ostringstream ss;
		ss << 'p' << this->_index;
		return ss.str();
	}

	void display(int indent = 0){
		for(int i = 0; i < indent; ++i)
			std::cout << ' ';
		std::cout << name() << '\n';
	}
private:
	int _index;
};

class funcnode: public node{
public:
	funcnode(string name, Func func, node* children[], int childcount){
		this->_name = name;
		this->_func = func;
		for(int i = 0; i < childcount; ++i){
			this->_children.push_back(children[i]);
		}
	}

	funcnode(string name, Func func, vector<node*> children){
		this->_name = name;
		this->_func = func;
		for(int i = 0; i < children.size(); ++i){
			this->_children.push_back(children[i]);
		}
	}
	
	float evaluate(vector<float> &input){
		vector<float> results;
		for(int i = 0; i < this->_children.size(); ++i)
			results.push_back(this->_children[i]->evaluate(input));
		
		return this->_func(results);
	}

	string name(){
		return this->_name;
	}

	~funcnode(){
		for(int i = 0; i < this->_children.size(); ++i)
			delete this->_children[i];
	}
	
	void display(int indent = 0){
		for(int i = 0; i < indent; ++i)
			std::cout << ' ';
		std::cout << name() << '\n';
		for(int i = 0; i < this->_children.size(); ++i)
			this->_children[i]->display(indent+1);
	}

private:
	vector<node*> _children;
	string _name;
	Func _func;
};

/************************** functions begin *******************************/
class fw{
public:
	fw(string name, Func func, int pc){
		this->name = name;
		this->func = func;
		this->pc = pc;
	}
	
	string name;
	Func func;
	int pc;
};

float add(vector<float> &input){
	float sum = 0;
	for(int i = 0; i < input.size(); ++i)
		sum += input[i];
	return sum;
}

float sub(vector<float> &input){
	if(input.size() == 0)
		return 0.0;

	float result = input[0];
	for(int i = 1; i < input.size(); ++i)
		result -= input[i];
	return result;
}

float mul(vector<float> &input){
	float result = 1.0;
	for(int i = 0; i < input.size(); ++i)
		result *= input[i];

	return result;
}

fw funcs[3] = {fw("add", add, 2), fw("sub", sub, 2), fw("mul", mul, 2)};
/************************** functions end *********************************/

node *randomnode(int pc, int maxdepth=4, float fpr=0.5, float ppr=0.6){
	if(random()%1000 < 500 && maxdepth > 0){
		// generate a funcnode
		fw func = funcs[random()%3];
	
		vector<node*> children;
		for(int i = 0; i < func.pc; ++i)
			children.push_back(randomnode(pc, maxdepth-1, fpr, ppr));
		return new funcnode(func.name, func.func, children);

	}else if(random()%1000 < 1000*ppr){
		return new paramnode(random() % pc);
	}else{
		return new constnode(random() % 10);
	}
}

float socrefunc(node* tree){
	return 0.0;
}

int main(){
	srand(time(0));

	node* tree = randomnode(3);
	tree->display();
}
