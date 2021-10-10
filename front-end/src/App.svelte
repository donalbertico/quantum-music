<script>
	import Crunker from 'crunker'
	export let name;

	let crunker = new Crunker();

	console.log('asdf');

	crunker
		.fetchAudio('audio/C_D100.wav','audio/C_D101.wav','audio/C_E110.wav')
		.then(buffers => crunker.concatAudio(buffers))
		.then(concat => crunker.export(concat,"audio/mp3"))
		.then(output => {
			crunker.download(output.blob,'asdfsd')
			console.log(output.url);
		})
		.catch(err=>{throw new Error(err)})
</script>

<main>
	<h1>Hello {name}!</h1>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
