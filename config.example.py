import modules.test

servers = [
	{
		"host": "example.com",
		"port": 6667,
		"nick": "KittyBot",
		"channels": [
            { "name": "#KittyBot" }
        ]
	}
]

used_modules = [
	modules.test.TestModule()
]