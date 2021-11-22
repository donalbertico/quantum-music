<script>
	import Crunker from 'crunker'
	import Knob from 'svelte-knob'
	import { Jumper } from 'svelte-loading-spinners'
	import Button from '@smui/button';

	let crunker = new Crunker();
	export let percentage = 50;
	export let loadingSp = false;
	export let binary = null
	export let clarinetSelected = true
	export let stringsSelected = false
	export let start = true
	let ids = null
	let assets = []
	let downloads = []
	let resultBuffer = null
	let loading = false
	let ready = false
	let idIndex = 0
	let fetching = false


	async function addCustomEvents(node) {
		function handleMouseDown() {
			node.addEventListener('mousemove', handleMouseMove)
		}
		function handleMouseMove(e){
			if(!fetching) getIds()
		}
		function handleMouseUp(){
			node.removeEventListener('mousemove',handleMouseMove)
			fetching = false
		  getIds()
		}
		node.addEventListener('mousedown',handleMouseDown)
		node.addEventListener('mouseup',handleMouseUp)
	}

	async function getIds(){
		fetching = true
		if (clarinetSelected) assets.push('cl')
		if (stringsSelected) assets.push('st')
		console.log(assets);
		// const res = await fetch(`https://quantum-music-concept.herokuapp.com/next?prob=${percentage}`,{
		const res = await fetch(`http://127.0.0.1:5000/next?prob=${percentage} ${assets.length>0 ? ('&assets='+encodeURIComponent(assets)) : ('')}`,{
			method: 'GET'
		})
		const json = await res.json();
		ids = json.ids;
		binary = json.binary;
		assets = []
		setTimeout( () => {
			fetching = false
		},600)
	}

	function plo(){
		binary = null
		// loadingSp = true
		getIds()

	}

	function generateAudio() {
		resultBuffer = null

		loadingSp = true
		console.log(ids);
		if (!ids) {
			loadingSp = false
			getIds()
			return
		}
		for (idIndex = 0; idIndex < ids.length -7; idIndex += 3 ){
			if (idIndex == 0) {
				crunker
					.fetchAudio(`audio/${ids[0]}`,`audio/${ids[1]}`,`audio/${ids[2]}`)
					.then(buffers => {
						return crunker.concatAudio(buffers)
					})
					.then(concat => {
						resultBuffer = concat
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
					})
					.catch(err => {throw new Error(err)})
			}
		}
		setTimeout(function () {
			loadingSp = false
			downloadOutput()
		}, 1100);
	}

	$:{
		// if(ids && !loading) {
		// 	loading = true
		// 	// console.log('cuantas cuentas?',idIndex);
		// 	if (idIndex == 0) {
		// 		crunker
		// 			.fetchAudio(`audio/${ids[0]}`,`audio/${ids[1]}`,`audio/${ids[2]}`)
		// 			.then(buffers => {
		// 				return crunker.concatAudio(buffers)
		// 			})
		// 			.then(concat => {
		// 				resultBuffer = concat
		// 				idIndex += 3
		// 				loading = false
		// 			})
		// 			.catch(err => {throw new Error(err)})
		// 	}else {
		// 		crunker
		// 			.fetchAudio(`audio/${ids[idIndex]}`,`audio/${ids[idIndex+1]}`,`audio/${ids[idIndex+2]}`)
		// 			.then(buffers => {
		// 				return crunker.concatAudio([resultBuffer, ...buffers])
		// 			})
		// 			.then(concat => {
		// 				resultBuffer = concat
		// 				if(idIndex >= ids.length-6){
		// 					ids = null
		// 					// ready = true
		// 					loading = false
		// 				}
		// 				idIndex += 3
		// 				loading = false
		// 			})
		// 			.catch(err => {throw new Error(err)})
		// 	}
		// }

		if(ready) {
			console.log('?');
			ready = false
			// downloadOutput()
			idIndex = 0
			loadingSp = false
		}
	}

	async function downloadOutput(){
		let output = await crunker.export(resultBuffer,"audio/mp3")
		crunker.download(output.blob,'result')
	}


</script>

<main style=' display:flex; flex-flow:column '>
		{#if start}
			<div style='flex:1'></div>
			<div style='flex:1; display:flex'>
				<div style='flex:1'></div>
				<div >
					<div class='button' on:click={() => {start = !start}}>ROTATE</div>
				</div>
				<div style='flex:1'></div>
			</div>
			<div style='flex:3'></div>
		{:else}
			{#if loadingSp}
				<div style='flex:2; display:flex'>
						<div style='flex:2'></div>
					{#if percentage > 50}
						<Jumper style='flex:1' size="200" color="#E91E63" unit="px" duration='2s'></Jumper>
					{:else}
						<Jumper size="200" color="#FFCCBC" unit="px" duration='2s'></Jumper>
					{/if}
						<div style='flex:2'></div>
				</div>
			{:else}
				<div style = 'flex:1'>
					<div style = 'display:flex' >
						<div style= 'width : 100%'></div>
						<div class={clarinetSelected ? ('selected') : ('unselected')}
							on:click={() => {clarinetSelected = !clarinetSelected; getIds();}}>
							Clarinet
						</div>
						<div style = 'width : 3%'></div>
						<div class={stringsSelected ? ('selected') : ('unselected')}
							on:click={() => {stringsSelected = !stringsSelected; getIds();}}>
							Strings
						</div>
						<div style= 'width : 100%'></div>
					</div>
				</div>
				<div use:addCustomEvents
					style='flex:2'>
					<Knob bind:value={percentage} textColor="#FFCCBC"
					secondaryColor="#FFCCBC" primaryColor='#E91E63' size={200}/>
				</div>
				<div style = 'flex:1'>
					<div style = 'display:flex' >
						<div style= 'width : 100%'></div>
						<div class='button' on:click={generateAudio} hidden={ids? false : true}> MEASURE </div>
						<div style= 'width : 100%'></div>
					</div>
				</div>
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
			{/if}
		{/if}


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
	.selected {
		color :  #FFCCBC;
		background-color: rgba(40,25,68,1);
		outline: none;
		border-radius: 50px;
		min-width: 100px;
		border: 0;
		padding: 9px;
		max-width: 150px;
		box-shadow: 0 2px 2px 0 #D32F2F;
	}
	.button {
		color: #FFCCBC;
		background-color: #E91E63;
		outline: none;
		border-radius: 50px;
		min-width: 100px;
		border: 0;
		padding: 20px;
		max-width: 150px;
		box-shadow: 0 3px 2px 0 #FFCCBC;
	}
	.unselected {
		color :  #FFCCBC;
		background-color: rgba(156,39,176,1);
		outline: none;
		border-radius: 50px;
		min-width: 100px;
		border: 0;
		padding: 9px;
		max-width: 150px;
		box-shadow: 0 2px 2px 0 rgba(40,25,68,1);
	}
</style>
