import {Command, flush, Errors} from '@oclif/core'
import {getIntrospectionQuery, IntrospectionQuery} from 'graphql'
import {request} from 'graphql-request'
import {fromIntrospectionQuery} from 'graphql-2-json-schema'

export default class SubgraphToJSONSchema extends Command {
  static description = 'Say hello'

  static args = [
    {
      name: 'subgraphUrl',
      description: 'URL of the the subgraph',
      required: true,
    },
  ]

  async run(): Promise<void> {
    const {args} = await this.parse(SubgraphToJSONSchema)

    const options = {
      // Whether or not to ignore GraphQL internals that are probably not relevant
      // to documentation generation.
      // Defaults to `true`
      ignoreInternals: true,
      // Whether or not to properly represent GraphQL Lists with Nullable elements
      // as type "array" with items being an "anyOf" that includes the possible
      // type and a "null" type.
      // Defaults to `false` for backwards compatibility, but in future versions
      // the effect of `true` is likely going to be the default and only way. It is
      // highly recommended that new implementations set this value to `true`.
      nullableArrayItems: true,
    }

    // schema is your GraphQL schema.
    const query = getIntrospectionQuery()

    const introspection: IntrospectionQuery = await request(
      args.subgraphUrl,
      query,
    )

    const jsonSchema = fromIntrospectionQuery(introspection, options)

    console.log(JSON.stringify(jsonSchema, null, 4))
  }
}

// Start the CLI
SubgraphToJSONSchema.run().then(flush, Errors.handle)
