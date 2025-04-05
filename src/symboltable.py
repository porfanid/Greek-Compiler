#########################################################################
# Symbol Table                                                          #
# This part of the code manages the symbol table for the compiler.      #
# The symbol table keeps track of all identifiers and their attributes  #
# such as type, scope level, offsets, etc.                             #
#########################################################################

import logging

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class SymbolTableEntity:
    """Represents an entity in the symbol table (variable, function, etc.)."""

    def __init__(self, name, entity_type=None, scope=None, offset=0, parameters=None):
        self.name = name
        self.entity_type = entity_type  # 'variable', 'function', 'procedure', etc.
        self.scope = scope              # Scope level
        self.offset = offset            # Memory offset
        self.parameters = parameters or []  # Parameters (for functions/procedures)

    def __str__(self):
        """String representation of the entity."""
        return f"{self.name} ({self.entity_type}), scope={self.scope}, offset={self.offset}"


class Scope:
    """Represents a scope in the program (global, function, block, etc.)."""

    def __init__(self, name, level, parent=None):
        self.name = name        # Name of the scope (e.g., function name)
        self.level = level      # Nesting level (0 for global)
        self.parent = parent    # Parent scope
        self.entities = {}      # Entities declared in this scope
        self.next_offset = 0    # Next available offset
        logger.debug(f"Created new scope: {name} (level {level})")

    def insert(self, entity):
        """Insert an entity into the current scope, or update if it already exists."""
        if entity.name in self.entities:
            logger.warning(
                f"{entity.entity_type.capitalize()} '{entity.name}' already exists in scope '{self.name}', skipping.")
            return self.entities[entity.name]  # Return existing entity

        self.entities[entity.name] = entity
        return entity


class SymbolTable:
    """Symbol table implementation that manages scopes and symbol declarations."""

    def __init__(self):
        """Initialize with global scope."""
        self.current_scope_level = 0
        self.scopes = [Scope("global", 0)]
        self.current_scope = self.scopes[0]
        logger.info("Symbol table initialized")

    @property
    def current_scope(self):
        """Get the current scope."""
        return self.scopes[self.current_scope_level]

    @current_scope.setter
    def current_scope(self, scope):
        """Set the current scope."""
        if self.current_scope_level < len(self.scopes):
            self.scopes[self.current_scope_level] = scope
        else:
            self.scopes.append(scope)

    def enter_scope(self, name):
        """Enter a new scope."""
        parent = self.current_scope
        self.current_scope_level += 1
        new_scope = Scope(name, self.current_scope_level, parent)
        self.current_scope = new_scope
        logger.debug(f"Entered scope: {name} (level {self.current_scope_level})")
        return new_scope

    def exit_scope(self):
        """Exit the current scope and return to parent scope."""
        if self.current_scope_level > 0:
            exited_scope_name = self.current_scope.name
            self.current_scope_level -= 1
            logger.debug(f"Exited scope: {exited_scope_name}, returned to level {self.current_scope_level}")
            return True
        logger.warning("Attempted to exit global scope")
        return False

    def insert(self, name, entity_type=None, parameters=None):
        """Insert a new entity into the current scope."""
        entity = SymbolTableEntity(name, entity_type, self.current_scope_level, parameters=parameters)
        return self.current_scope.insert(entity)

    def lookup(self, name, current_scope_only=False):
        """
        Look up an entity by name.
        If current_scope_only is True, only look in the current scope.
        Otherwise, also check parent scopes.
        """
        scope = self.current_scope
        while scope:
            if name in scope.entities:
                logger.debug(f"Found '{name}' in scope '{scope.name}'")
                return scope.entities[name]
            if current_scope_only:
                break
            scope = scope.parent

        logger.debug(f"Entity '{name}' not found")
        return None

    def __str__(self):
        """Generate a string representation of the entire symbol table."""
        result = ["Symbol Table:"]
        for scope in self.scopes:
            result.append(f"\nScope: {scope.name} (level {scope.level})")
            for name, entity in scope.entities.items():
                result.append(f"  {entity}")
        return "\n".join(result)


def build_symbol_table(ast):
    """
    Build a symbol table from an AST.

    Args:
        ast: The abstract syntax tree

    Returns:
        A populated SymbolTable instance
    """
    logger.info("Building symbol table from AST")
    symbol_table = SymbolTable()

    # Process the AST to build the symbol table
    _process_ast_node(ast, symbol_table)

    logger.info("Symbol table construction complete")
    return symbol_table


def _process_ast_node(node, symbol_table):
    """
    Recursively process an AST node to populate the symbol table.

    Args:
        node: The current AST node
        symbol_table: The symbol table to populate
    """
    node_type = node.get('type')

    # Process based on node type
    if node_type == 'PROGRAM':
        # Program name
        program_name = node['children'][0]['value']
        logger.debug(f"Processing program: {program_name}")
        symbol_table.insert(program_name, 'program')

        # Process program block
        if len(node['children']) > 1:
            _process_ast_node(node['children'][1], symbol_table)

    elif node_type == 'DECLARATIONS':
        if 'children' in node:
            for var_list in node['children']:
                _process_ast_node(var_list, symbol_table)

    elif node_type == 'VAR_LIST':
        if 'children' in node:
            for var_node in node['children']:
                var_name = var_node['value']
                logger.debug(f"Declaring variable: {var_name}")
                try:
                    symbol_table.insert(var_name, 'variable')
                except ValueError as e:
                    logger.error(f"Error adding variable {var_name}: {str(e)}")

    elif node_type == 'FUNCTION':
        # Function name
        func_name = node['children'][0]['value']
        logger.debug(f"Processing function: {func_name}")

        # Parse parameters
        params = []
        if len(node['children']) > 1:
            param_node = node['children'][1]
            if 'children' in param_node and param_node['children']:
                for var_list in param_node['children']:
                    if 'children' in var_list:
                        for param in var_list['children']:
                            params.append(param['value'])

        # Add function to symbol table
        try:
            symbol_table.insert(func_name, 'function', params)
        except ValueError as e:
            logger.error(f"Error adding function {func_name}: {str(e)}")
            raise

        # Enter function scope
        symbol_table.enter_scope(func_name)

        # Add parameters to function scope
        for param in params:
            symbol_table.insert(param, 'parameter')

        # Process function body
        if len(node['children']) > 2:
            _process_ast_node(node['children'][2], symbol_table)

        # Exit function scope
        symbol_table.exit_scope()

    elif node_type == 'PROCEDURE':
        # Similar to function processing
        proc_name = node['children'][0]['value']
        logger.debug(f"Processing procedure: {proc_name}")

        # Parse parameters
        params = []
        if len(node['children']) > 1:
            param_node = node['children'][1]
            if 'children' in param_node and param_node['children']:
                for var_list in param_node['children']:
                    if 'children' in var_list:
                        for param in var_list['children']:
                            params.append(param['value'])

        # Add procedure to symbol table
        try:
            symbol_table.insert(proc_name, 'procedure', params)
        except ValueError as e:
            logger.error(f"Error adding procedure {proc_name}: {str(e)}")
            raise

        # Enter procedure scope
        symbol_table.enter_scope(proc_name)

        # Add parameters to procedure scope
        for param in params:
            symbol_table.insert(param, 'parameter')

        # Process procedure body
        if len(node['children']) > 2:
            _process_ast_node(node['children'][2], symbol_table)

        # Exit procedure scope
        symbol_table.exit_scope()

    # Process other node types recursively
    if 'children' in node:
        for child in node['children']:
            _process_ast_node(child, symbol_table)

#########################################################################
# End of Symbol Table                                                   #
#########################################################################