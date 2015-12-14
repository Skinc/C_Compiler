#include <time.h>
#include <stdio.h>

#define loopCount 1000
#define testCount 10

int wrapper_function() {
	int a, b, c, d, e, f, g, h, i, j, k, l, 
		m, n, o, p, q, r, s, t, u, v, w, x, y, z;

	c = i - j;
 	d = i + j;
 	a = i * i;
 	b = j * j;
 	e = a + b;
 	x = c * d;
 	f = x * e;
 	return f;

}


int main () {
	clock_t begin, end;
	double time_spent, times;
	int i;
	int result;

	for (i = 0; i < testCount; i++){
		int j;
	  	begin = clock();

	  	for (j = 0; j < loopCount; j++) {
	  		result = wrapper_function();
	  	}

		end = clock();
	  	time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
  		times = times + time_spent;
  	}
  	printf("Average time spent: %f\n", times/testCount );
  		
	return result;
}