import {Command, flush, Errors} from '@oclif/core'

export default class SubgraphToJSONSchema extends Command {
  static description = 'Say hello'

  static args = [{name: 'subgraphUrl', description: 'URL of the the subgraph', required: true}]

  async run(): Promise<void> {
    const {args} = await this.parse(SubgraphToJSONSchema)

    console.log(args.subgraphUrl)
  }
}

// Start the CLI
SubgraphToJSONSchema.run().then(flush, Errors.handle)
