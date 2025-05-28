#include "sys.h"
#include "delay.h"
#include "usart.h"
#include "led.h"
#include "beep.h"
#include "key.h"

void Delay(__IO u32 nCount); 

/**
  * @brief  主函数
  * @param  无
  * @retval 无
  */
int main(void)
{
	/* LED 端口初始化 */
	LED_GPIO_Config();
	/*蜂鸣器端口初始化 */
	BEEP_GPIO_Config(); 
	/*初始化按键*/
  Key_GPIO_Config();

	/* 控制LED灯 */
	while (1)
	{
		if( Key_Scan(KEY1_GPIO_PORT,KEY1_PIN) == KEY_ON  )
		{
			/*LED1反转*/
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

void Delay(__IO uint32_t nCount)	 //简单的延时函数
{
	for(; nCount != 0; nCount--);
}
