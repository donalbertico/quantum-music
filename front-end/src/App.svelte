<script>
	import Crunker from 'crunker'
	import Knob from 'svelte-knob'
	import { Jumper } from 'svelte-loading-spinners'

	let crunker = new Crunker();
	export let percentage = 50;
	export let loadingSp = false;
	export let binary = null
	let ids = null
	let downloads = []
	let resultBuffer = null
	let loading = false
	let ready = false
	let idIndex = 0


	async function getIds(){
		const res = await fetch(`https://quantum-music-concept.herokuapp.com/next?prob=${percentage}`,{
			method: 'GET'
		})
		const json = await res.json();
		ids = json.ids;
		binary = json.binary;
	}

	function handleClick(){
		binary = null
		loadingSp = true
		getIds()
	}

	$:{
		if(ids && !loading) {
			loading = true
			console.log('cuantas cuentas?',idIndex);
			if (idIndex == 0) {
				crunker
					.fetchAudio(`audio/${ids[0]}`,`audio/${ids[1]}`,`audio/${ids[2]}`)
					.then(buffers => {
						return crunker.concatAudio(buffers)
					})
					.then(concat => {
						resultBuffer = concat
						idIndex += 3
						loading = false
					})
					.catch(err => {throw new Error(err)})
			}else {
				crunker
					.fetchAudio(`audio/${ids[idIndex]}`,`audio/${ids[idIndex+1]}`,`audio/${ids[idIndex+2]}`)
					.then(buffers => {
						return crunker.concatAudio([resultBuffer, ...buffers])
					})
					.then(concat => {
						resultBuffer = concat
						if(idIndex >= ids.length-5){
							ids = null
							ready = true
						}
						idIndex += 3
						loading = false
					})
					.catch(err => {throw new Error(err)})
			}
		}

		if(ready) {
			ready = false
			downloadOutput()
			idIndex = 0
			loadingSp = false
		}
	}

	async function downloadOutput(){
		let output = await crunker.export(resultBuffer,"audio/mp3")
		crunker.download(output.blob,'result')
	}


</script>

<main style='display:flex;flex-flow:column'>
		{#if loadingSp}
			<div style='flex:2;display:flex'>
				<div style='flex:2'></div>
			{#if percentage > 50}
				<Jumper style='flex:1' size="200" color="#E91E63" unit="px" duration='2s'></Jumper>
			{:else}
				<Jumper size="200" color="#FFCCBC" unit="px" duration='2s'></Jumper>
			{/if}
				<div style='flex:2'></div>
			</div>
		{:else}
			<div on:click={handleClick} style='flex:2'>
				<Knob bind:value={percentage} textColor="#FFCCBC"
				secondaryColor="#FFCCBC" primaryColor='#E91E63' size={200}/>
			</div>
		{/if}

		<div style="flex:1;display:flex">
			{#if binary}
				{#each binary as bin}
					{#if bin}
						<div class="cl card"></div>
					{:else}
						<div class="st card"></div>
					{/if}
				{/each}
			{/if}
		</div>
		<div style='flex:2'></div>
</main>
<style>
	main {
		text-align: center;
		padding: 1em;
		margin: 0 auto;
		height: 100%;
		max-width: 240px;
		background: rgb(156,39,176);
 		background: linear-gradient(180deg, rgba(156,39,176,1) 0%, rgba(40,25,68,1) 65%);
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}

	.card {
		width: 2em;
		height: 2em;
		margin: 2px;
	}
	.st {
		background-color: #E91E63
	}
	.cl {
		background-color: #FFCCBC
	}
</style>
