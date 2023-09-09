<script lang="ts">
	import { Code, Slide, Vertical } from '@components'
	import Color from './Color.svelte'
	import Layout from './Layout.svelte'

	const termCode = `
class Term:
  if platform.system() == 'Windows':
      os.system('color')

  BLACK = "\\033[30m"
  R = "\\033[31m"
  G = "\\033[32m"
  BG = "\\033[1;32m"
  Y = "\\033[33m"
  B = "\\033[34m"
  M = "\\033[35m"
  C = "\\033[36m"
  W = "\\033[37m"
  ENDC = "\\033[0;0m"
  NORMAL = "\\033[1m"
  BOLD = "\\033[1m"


def dev_print(*values: object):
  print(f'{Term.M}[dev]{Term.ENDC}', *values)
      `
</script>

<Vertical>
	<Slide>
		<Layout>
			<h2>Dato de <Color>color 1</Color></h2>
			<p>
				Sabias que colorear la terminal es tan sencillo como agregar unos
				caracteres antes del texto?
			</p>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<Code lang="python">
				{`
          print("\\033[1;31mHola Mundo")
        `}
			</Code>
		</Layout>
	</Slide>
	<Slide>
		<Layout>
			<Code lang="python">
				{`
          print("\\033[1;31mHola Mundo")
        `}
			</Code>
			<img src="print-output-0.png" alt="" class="w-2/3 mx-auto" />
		</Layout>
	</Slide>
	<Slide>
		<p>Se puede hacer mejor?</p>
	</Slide>
	<Slide>
		<p>Si</p>
	</Slide>
	<Slide>
		<Code lang="python">
			{`
        class Term:
          if platform.system() == 'Windows':
              os.system('color')
        
          BLACK = "\\033[30m"
          R = "\\033[31m"
          G = "\\033[32m"
          BG = "\\033[1;32m"
          Y = "\\033[33m"
          B = "\\033[34m"
          M = "\\033[35m"
          C = "\\033[36m"
          W = "\\033[37m"
          ENDC = "\\033[0;0m"
          NORMAL = "\\033[1m"
          BOLD = "\\033[1m"
        
        
        def dev_print(*values: object):
          print(f'{Term.M}[dev]{Term.ENDC}', *values)
      `}
		</Code>
	</Slide>
	<Slide>
		<Layout>
			<p>Usandolo:</p>
			<Code lang="python">
				{`
          def minify_tailwindcss(cli: argparse.Namespace):
            ...
            dev_print(f'Minifying tailwindcss for production...')
  
            build_result = subprocess.run(shlex.split(command))
  
            if build_result.returncode != 0:
                dev_print(
            f'Tailwind build for production {Term.R}fail{Term.ENDC}')
              return build_result.returncode
  
            dev_print(
              f'Tailwind build for production {Term.G}ready{Term.ENDC}')
            return build_result.returncode
        `}
			</Code>
		</Layout>
	</Slide>
	<Slide>
		<img src="print-output-1.png" alt="" class="w-2/3 mx-auto" />
		<p>Salio bien</p>
	</Slide>
	<Slide>
		<Layout>
			<img src="print-output-2.png" alt="" class="w-2/3 mx-auto" />
			<p>Salio mal</p>
		</Layout>
	</Slide>
</Vertical>
