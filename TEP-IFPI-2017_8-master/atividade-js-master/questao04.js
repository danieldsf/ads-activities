Array.from(new Array(101),(k,i) => console.log( i==0 ? "" : (i%3==0 && i%5==0  ? "FizzBuzz" : (i%5==0 ? "Buzz" : ( i%5==0 ? "Fizz" : i)))));
