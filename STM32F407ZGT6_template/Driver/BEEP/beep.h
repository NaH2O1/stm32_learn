#ifndef __BEEP_H
#define	__BEEP_H


#include "stm32f4xx.h"


/* ������������ӵ�GPIO�˿�, �û�ֻ��Ҫ�޸�����Ĵ��뼴�ɸı���Ƶķ��������� */
#define BEEP_GPIO_PORT    	GPIOG			              /* GPIO�˿� */
#define BEEP_GPIO_CLK 	    RCC_AHB1Periph_GPIOG		/* GPIO�˿�ʱ�� */
#define BEEP_GPIO_PIN		  	GPIO_Pin_7			        /* ���ӵ���������GPIO */

/* �͵�ƽʱ���������� */
#define BEEP_ON  1
#define BEEP_OFF 0

/* ���κ꣬��������������һ��ʹ�� */
#define BEEP(a)	if (a)	\
					GPIO_ResetBits(BEEP_GPIO_PORT,BEEP_GPIO_PIN);\
					else		\
					GPIO_SetBits(BEEP_GPIO_PORT,BEEP_GPIO_PIN)				
					


void BEEP_GPIO_Config(void);
					
#endif /* __BEEP_H */
