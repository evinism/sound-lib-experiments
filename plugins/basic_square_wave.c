#include "soundexp/plugin.h"

extern void init(){}

int cycleSize = 200;
int count = 0;
extern float tick(float sample){
  count = (count + 1) % (cycleSize * 2);
  if(count / cycleSize == 1){
    return 1.0;
  } else {
    return -1.0;
  }
}