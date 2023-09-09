<script lang="ts">
	import { Code, Slide, Vertical } from '@components'
	import Color from './Color.svelte'
	import Layout from './Layout.svelte'
</script>

<Vertical>
	<Slide>
		<Layout>
			<h2>Dato de <Color>color 3</Color></h2>
			<p>lo facil esta bueno, no?, no???</p>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>por ejemplo hacer una cli sencilla</h2>
			<p>tenemos la lib <q>argparse</q> en la std de python</p>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<Code lang="python">
				{`
import argparse

print("\\033[1;31mHola Mundo")

parser = argparse.ArgumentParser(
    description='Process some integers.')
parser.add_argument(
    'integers', metavar='N', type=int, nargs='+',
    help='an integer for the accumulator')
parser.add_argument(
    '--sum', dest='accumulate', action='store_const',
    const=sum, default=max,
    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))
`}
			</Code>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>mira que lindo</h2>
			<img src="print-output-3.png" alt="" />
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>ah si, recuerden restablecer los colores</h2>
			<Code lang="python">
				{`
import argparse

print("\\033[1;31mHola Mundo")
...
`}
			</Code>
			<Code lang="python">
				{`
import argparse

print("\\033[1;31mHola Mundo\\033[0;0m")
...
`}
			</Code>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<h2>ahora si, mira que lindo</h2>
			<img src="print-output-4.png" alt="" />
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<p>yo: uh para, entonces vamos a agregar alguna que otra opcion</p>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<p>una que otra?</p>
		</Layout>
	</Slide>
	<Slide>
		<Code lang="python" offset="228">
			{`
def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Enhanced dev environment for flask apps.',
        allow_abbrev=True
    )
    # +75 lineas despues
`}
		</Code>
		<Code lang="python" offset="319">
			{`
    parser_dev.add_argument(
        '-tm', '--tailwind-minify', dest='tailwind_minify', action='store_true', default=False,
        help='Enables minification of the generated css file.'
    )

    return parser
`}
		</Code>
	</Slide>
	<Slide>
		<Layout>
			<p>recomendacion, no se emocionen</p>
		</Layout>
	</Slide>
</Vertical>
