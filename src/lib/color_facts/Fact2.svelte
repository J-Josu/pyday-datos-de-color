<script lang="ts">
	import { Code, Slide, Vertical } from '@components'
	import Color from './Color.svelte'
	import Layout from './Layout.svelte'
</script>

<Vertical>
	<Slide>
		<Layout>
			<h2>Dato de <Color>color 2</Color></h2>
			<p>Chat gpt, copilot y toda sus amigos ia estan buenos</p>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>hasta que le pedis un codigo...</h2>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<Code lang="python">
				{`
trigger_full_reload = False

async def send_full_reload(websocket):
    global trigger_full_reload

    while True:
        if trigger_full_reload:
            trigger_full_reload = False
            await websocket.send(json.dumps({
                "type": "TRIGGER_FULL_RELOAD",
                "data": datetime.datetime.now().isoformat()
            }))

        await asyncio.sleep(REFRESH_RATE_SEC)

# en otro lugar...
trigger_full_reload = True
`}
			</Code>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>y funciona (o aveces)</h2>
			<p>el problema es que esa boleana solo funcionaba una vez</p>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>y con mas de una pagina?</h2>
			<p>chatgpt: hmmm nose</p>
			<p>copilot: me mataste</p>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>la respuesta...</h2>
		</Layout>
	</Slide>

	<Slide>
		<Layout>
			<h2 class="text-8xl">los docs</h2>
		</Layout>
	</Slide>

	<Slide>
		<Layout>
			<h2 class="text-8xl">si la</h2>
			<h2><span class="text-8xl font-black"> DOCUMENTACION </span></h2>
		</Layout>
	</Slide>

	<Slide>
		<Layout>
			<Code lang="python">
				{`
LR_CONNECTIONS: 'set[ws_server.WebSocketServerProtocol]' = set()

async def handle_connection(websocket):
    LR_CONNECTIONS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        LR_CONNECTIONS.remove(websocket)

# en otro lugar...
ws_protocol.broadcast(LR_CONNECTIONS, json.dumps({
    "type": "TRIGGER_FULL_RELOAD",
    "data": datetime.datetime.now().isoformat()
}))
`}
			</Code>
		</Layout>
	</Slide>

	<Slide>
		<Layout>
			<h2>Ahora mejor</h2>
			<p>o bueno hasta que un bug me mande a leerla denuevo...</p>
			<small class="mt-16">ya paso.</small>
		</Layout>
	</Slide>
</Vertical>
