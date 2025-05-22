#ifndef __LED_H
#define __LED_H

#include "stm32f4xx.h"
/*ʹ�ú��Ŀ������ϵ�led
LED0->PF9
LED1->PF10
PWR ->��Դ������
*/


//���Ŷ���
/*******************************************************/
//R ��ɫ��
#define LED0_PIN                  GPIO_Pin_9                
#define LED0_GPIO_PORT            GPIOF                      
#define LED0_GPIO_CLK             RCC_AHB1Periph_GPIOF

//G ��ɫ��
#define LED1_PIN                  GPIO_Pin_10               
#define LED1_GPIO_PORT            GPIOF                      
#define LED1_GPIO_CLK             RCC_AHB1Periph_GPIOF
/*******************************************************/


/** ����LED������ĺ꣬
	* LED�͵�ƽ��������ON=0��OFF=1
	* ��LED�ߵ�ƽ�����Ѻ����ó�ON=1 ��OFF=0 ����
	*/
#define LED_ON  0
#define LED_OFF 1

/* ���κ꣬��������������һ��ʹ�� */
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

