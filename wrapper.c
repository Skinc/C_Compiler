#include <time.h>
void wrapper_function() {
	int a, b, c, d, e, f, g, h, i, j, k, l, 
		m, n, o, p, q, r, s, t, u, v, w, x, y, z;

}
#define testCount 10
int main () {
	double times
	for (int i = 0; i < testCount; i++){

		clock_t begin, end;
	  	double time_spent;
	  	begin = clock();

		wrapper_function();
		end = clock();
	  	time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
  		printf("Time spent: %f", time_spent );
  		times = times + time_spent;
  	}
  	printf("Time spent: %f", times/testCount );
  		

	return 0;
}