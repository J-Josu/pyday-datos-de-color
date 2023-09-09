<script lang="ts">
	import { Presentation, Slide } from '@components'
	import Color from '@lib/color_facts/Color.svelte'
	import Fact1 from '@lib/color_facts/Fact1.svelte'
	import Fact2 from '@lib/color_facts/Fact2.svelte'
	import Fact3 from '@lib/color_facts/Fact3.svelte'
	import Fact4 from '@lib/color_facts/Fact4.svelte'
	import Fact5 from '@lib/color_facts/Fact5.svelte'
</script>

<Presentation>
	<Slide>
		<h1 class="text-8xl font-bold">Datos de <Color>COLOR</Color></h1>
	</Slide>
	<Slide>
		<h2 class="text-6xl font-bold">Yo soy josue</h2>
		<div class="flex flex-col my-8 gap-4">
			<p>Me dicen josu</p>
			<p>Me gusta programar</p>
			<p>
				Y les vengo a contar cosas que aprendi metiendole tailwindcss y live
				reloading para una aplicacion en flask
			</p>
		</div>
		<p>Comenzamos?</p>
	</Slide>

	<Fact1 />

	<Fact2 />

	<Fact3 />

	<Fact4 />

	<Fact5 />

	<Slide>
		<p>
			y recuerden, si una idea se les ocurre, por mas rara, simple o dificil sea
		</p>
	</Slide>

	<Slide>
		<p>si piensan que minimamente es factible</p>
	</Slide>

	<Slide>
		<p>intentalo</p>
	</Slide>

	<Slide>
		<p>aunque no lo consigas, seguro algo aprendes</p>
	</Slide>

	<Slide>
		<p>yo ahora se colorear la terminal 😎</p>
	</Slide>

	<Slide>
		<h2
			class="text-8xl font-black bg-clip-text text-transparent bg-gradient-to-r from-pink-500 to-violet-500"
		>
			Gracias por el espacio
		</h2>
	</Slide>

	<Slide>
		<img
			src="repository-qr.png"
			alt="codigo qr del repositorio"
			class="mx-auto"
		/>
		<p class="mt-[1em]">Link al repositorio</p>
	</Slide>
</Presentation>

<style lang="postcss">
	:global(.reveal-viewport) {
		@apply bg-zinc-950;
	}
	:global(h2) {
		@apply text-stone-100;
	}
	:global(p) {
		@apply text-stone-200;
	}
</style>
