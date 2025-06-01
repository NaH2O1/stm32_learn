#include "sys.h"
#include "delay.h"
#include "usart.h"
#include "./led.h"
#include "./beep.h"
#include "../Driver/EXIT/exti.h"

void Delay(__IO u32 nCount); 

/**
  * @brief  主函数
  * @param  无
  * @retval 无
  */
int main(void)
{
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);//设置系统中断优先级分组2
	delay_init(168);    //初始化延时函数
	uart_init(115200); 	//串口初始化 
	LED_GPIO_Config();				  //初始化LED端口  
	BEEP_GPIO_Config();        //初始化蜂鸣器端口
	EXTIX_Init();       //初始化外部中断输入 
	LED0(LED_ON);					    //先点亮红灯
	while(1)
	{
		printf("OK\r\n");	//打印OK提示程序运行
		delay_ms(1000);	  //每隔1s打印一次
	}
}

void Delay(__IO uint32_t nCount)	 //简单的延时函数
{
	for(; nCount != 0; nCount--);
}





//if( Key_Scan(KEY1_GPIO_PORT,KEY1_PIN) == KEY_ON  )
//		{
//			/*LED1反转*/
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