# MQTT
* __NEVER__ subscribe to the _state_ topic. It will cause an infinite loop. Use the _state_ topic only to __publish__!
* 