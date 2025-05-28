#ifndef __LED_H
#define __LED_H

#include "stm32f4xx.h"
/*使用核心开发板上的led
LED0->PF9
LED1->PF10
PWR ->电源常亮灯
*/


//引脚定义
/*******************************************************/
//R 红色灯
#define LED0_PIN                  GPIO_Pin_9                
#define LED0_GPIO_PORT            GPIOF                      
#define LED0_GPIO_CLK             RCC_AHB1Periph_GPIOF

//G 绿色灯
#define LED1_PIN                  GPIO_Pin_10               
#define LED1_GPIO_PORT            GPIOF                      
#define LED1_GPIO_CLK             RCC_AHB1Periph_GPIOF
/*******************************************************/


/** 控制LED灯亮灭的宏，
	* LED低电平亮，设置ON=0，OFF=1
	* 若LED高电平亮，把宏设置成ON=1 ，OFF=0 即可
	*/
#define LED_ON  0
#define LED_OFF 1

/* 带参宏，可以像内联函数一样使用 */
#define LED0(a)	if (a)	\
					GPIO_SetBits(LED0_GPIO_PORT,LED0_PIN);\
					else		\
					GPIO_ResetBits(LED0_GPIO_PORT,LED0_PIN)

#define LED1(a)	if (a)	\
					GPIO_SetBits(LED1_GPIO_PORT,LED1_PIN);\
					else		\
					GPIO_ResetBits(LED1_GPIO_PORT,LED1_PIN)
					

void LED_GPIO_Config(void);

#endif /* __LED_H */

