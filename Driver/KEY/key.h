#ifndef __KEY_H
#define	__KEY_H

#include "stm32f4xx.h"

//���Ŷ���
// KEY_UP PA0
// KEY0 PE4
/*******************************************************/
#define KEY1_PIN                  GPIO_Pin_0                 
#define KEY1_GPIO_PORT            GPIOA                      
#define KEY1_GPIO_CLK             RCC_AHB1Periph_GPIOA

#define KEY2_PIN                  GPIO_Pin_4                 
#define KEY2_GPIO_PORT            GPIOE                      
#define KEY2_GPIO_CLK             RCC_AHB1Periph_GPIOE
/*******************************************************/

 /** �������±��ú�
	* ��������Ϊ�ߵ�ƽ������ KEY_ON=1�� KEY_OFF=0
	* ����������Ϊ�͵�ƽ���Ѻ����ó�KEY_ON=0 ��KEY_OFF=1 ����
	*/
#define KEY_ON	1
#define KEY_OFF	0

void Key_GPIO_Config(void);
uint8_t Key_Scan(GPIO_TypeDef* GPIOx,u16 GPIO_Pin);

#endif /* __LED_H */
