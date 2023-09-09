<script lang="ts">
	import { Code, Slide, Vertical } from '@components'
	import Color from './Color.svelte'
	import Layout from './Layout.svelte'
</script>

<Vertical>
	<Slide>
		<Layout>
			<h2>Dato de <Color>color 4</Color></h2>
			<p>Un paron aveces ayuda</p>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>recuerdan este fragmento de antes?</h2>
			<Code lang="python">
				{`
    ...
    while True:
        if trigger_full_reload:
            trigger_full_reload = False
            await websocket.send(json.dumps({
                "type": "TRIGGER_FULL_RELOAD",
                "data": datetime.datetime.now().isoformat()
            }))
    ...
`}
			</Code>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>imagina que encontras en los docs</h2>
			<p>websockets.broadcast(websockets, message, raise_exceptions=False)</p>
			<p>Broadcast a message to several WebSocket connections.</p>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>buenisimo, vamos a probarlo seguro anda</h2>
		</Layout>
	</Slide>

	<Slide>
		<Layout>
			<h2>pumba lo cambiamos</h2>
			<Code lang="python">
				{`
...
while True:
    if trigger_full_reload:
        trigger_full_reload = False
        await websockets.send(json.dumps({
            "type": "TRIGGER_FULL_RELOAD",
            "data": datetime.datetime.now().isoformat()
        }))
...
`}
			</Code>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>y...</h2>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<img src="print-output-5.png" alt="" />
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>pero para...</h2>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>pero para...</h2>
			<p>los docs dicen websockets</p>
			<p>no websocket</p>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>casualmente mi parametro se llamaba websocket</h2>
			<p>y los confundi</p>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>pero no me di cuenta, y tarde en darme cuenta</h2>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>un ratito nomas...</h2>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>15min - 30min despues</h2>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>me di cuenta y lo cambie</h2>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>acto seguido comitee y me fui</h2>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>nota mental 1:</h2>
			<h2>hacer un break cada tanto</h2>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>nota mental 2:</h2>
			<h2>acordarse la nota 1</h2>
		</Layout>
	</Slide>
</Vertical>
