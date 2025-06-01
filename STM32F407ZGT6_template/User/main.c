#include "sys.h"
#include "delay.h"
#include "usart.h"
#include "./led.h"
#include "./beep.h"
#include "../Driver/EXIT/exti.h"

void Delay(__IO u32 nCount); 

/**
  * @brief  ������
  * @param  ��
  * @retval ��
  */
int main(void)
{
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);//����ϵͳ�ж����ȼ�����2
	delay_init(168);    //��ʼ����ʱ����
	uart_init(115200); 	//���ڳ�ʼ�� 
	LED_GPIO_Config();				  //��ʼ��LED�˿�  
	BEEP_GPIO_Config();        //��ʼ���������˿�
	EXTIX_Init();       //��ʼ���ⲿ�ж����� 
	LED0(LED_ON);					    //�ȵ������
	while(1)
	{
		printf("OK\r\n");	//��ӡOK��ʾ��������
		delay_ms(1000);	  //ÿ��1s��ӡһ��
	}
}

void Delay(__IO uint32_t nCount)	 //�򵥵���ʱ����
{
	for(; nCount != 0; nCount--);
}





//if( Key_Scan(KEY1_GPIO_PORT,KEY1_PIN) == KEY_ON  )
//		{
//			/*LED1��ת*/
//			LED1( LED_ON );	
//			LED0 ( LED_OFF );	
//			BEEP(BEEP_ON);
//			Delay(0xFFFFFF);
//		}   
 //   	if( Key_Scan(KEY2_GPIO_PORT,KEY2_PIN) == KEY_ON )
//		{
//			LED1( LED_OFF );	
//			LED0 ( LED_ON );
//			BEEP(BEEP_OFF);
//			Delay(0xFFFFFF);
//		} 