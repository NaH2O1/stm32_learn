#ifndef __BEEP_H
#define	__BEEP_H


#include "stm32f4xx.h"


/* 定义蜂鸣器连接的GPIO端口, 用户只需要修改下面的代码即可改变控制的蜂鸣器引脚 */
#define BEEP_GPIO_PORT    	GPIOG			              /* GPIO端口 */
#define BEEP_GPIO_CLK 	    RCC_AHB1Periph_GPIOG		/* GPIO端口时钟 */
#define BEEP_GPIO_PIN		  	GPIO_Pin_7			        /* 连接到蜂鸣器的GPIO */

/* 低电平时，蜂鸣器响 */
#define BEEP_ON  1
#define BEEP_OFF 0

/* 带参宏，可以像内联函数一样使用 */
#define BEEP(a)	if (a)	\
					GPIO_ResetBits(BEEP_GPIO_PORT,BEEP_GPIO_PIN);\
					else		\
					GPIO_SetBits(BEEP_GPIO_PORT,BEEP_GPIO_PIN)				
					


void BEEP_GPIO_Config(void);
					
#endif /* __BEEP_H */
