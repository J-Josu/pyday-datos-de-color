<script lang="ts">
	import { Code, Slide, Vertical } from '@components'
	import Layout from './Layout.svelte'
	import Color from './Color.svelte'
</script>

<Vertical>
	<Slide>
		<Layout>
			<h2>Dato de <Color>color 5</Color></h2>
			<p>dormir esta bien</p>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>La idea era poner 5 datos de <Color>color</Color></h2>
      <p>pero se me hizo tarde</p>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>Son las 0:52hs</h2>
      <p>mejor si me voy a dormir</p>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>No te miento, aprendi mas cosas</h2>
      <small>pero no me las acuerdo</small>
		</Layout>
	</Slide>
</Vertical>
