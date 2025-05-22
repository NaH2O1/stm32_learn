#include "sys.h"
#include "delay.h"
#include "usart.h"
#include "led.h"
#include "beep.h"
#include "key.h"

void Delay(__IO u32 nCount); 

/**
  * @brief  ������
  * @param  ��
  * @retval ��
  */
int main(void)
{
	/* LED �˿ڳ�ʼ�� */
	LED_GPIO_Config();
	/*�������˿ڳ�ʼ�� */
	BEEP_GPIO_Config(); 
	/*��ʼ������*/
  Key_GPIO_Config();

	/* ����LED�� */
	while (1)
	{
		if( Key_Scan(KEY1_GPIO_PORT,KEY1_PIN) == KEY_ON  )
		{
			/*LED1��ת*/
			LED1( LED_ON );	
			LED0 ( LED_OFF );	
			BEEP(BEEP_ON);
			Delay(0xFFFFFF);
		}   
    
    if( Key_Scan(KEY2_GPIO_PORT,KEY2_PIN) == KEY_ON )
		{
			LED1( LED_OFF );	
			LED0 ( LED_ON );
			BEEP(BEEP_OFF);
			Delay(0xFFFFFF);
		}

	}
}

void Delay(__IO uint32_t nCount)	 //�򵥵���ʱ����
{
	for(; nCount != 0; nCount--);
}
