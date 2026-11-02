'use client'

import { TemplateRadioGroup } from '@/components/template-select/template-radio-group'
import {
  getTemplatesTemplatesGetOptions,
  getUserTemplatesUserTemplatesGetOptions,
} from '@/lib/client/@tanstack/react-query.gen'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Template } from '@/types/templates'
import { useQuery } from '@tanstack/react-query'
import { FileText } from 'lucide-react'
import { useState } from 'react'

export const TemplateSelect = ({
  value,
  onChange,
}: {
  onChange: (template: Template) => void
  value: Template
}) => {
  return (
    <div>
      <DefaultTemplateSelect value={value} onChange={onChange} />
      <h4 className="font-bold">Your templates</h4>
      <UserTemplateSelect value={value} onChange={onChange} />
    </div>
  )
}

export const DefaultTemplateSelect = ({
  onChange,
  value,
}: {
  onChange: (template: Template) => void
  value: Template
}) => {
  const { data: templates = [], isLoading } = useQuery(
    getTemplatesTemplatesGetOptions()
  )

  const categories = [...new Set(templates.map((t) => t.category))].sort((a, b) => {
    const order = ['Standard', 'Adult Services, Commissioning and Public Health', 'Children and Young Peoples Services', 'Legal and Governance', 'Legacy Templates']
    const ai = order.indexOf(a)
    const bi = order.indexOf(b)
    if (ai === -1 && bi === -1) return a.localeCompare(b)
    if (ai === -1) return 1
    if (bi === -1) return -1
    return ai - bi
  })

  const [selectedCategory, setSelectedCategory] = useState('')
  const activeCategory = selectedCategory || categories[0] || ''
  const filtered = templates.filter((t) => t.category === activeCategory)

  return (
    <div className="mb-4">
      <div className="mb-4 flex items-center gap-3">
        <span className="text-sm font-medium">Template Category:</span>
        <Select value={activeCategory} onValueChange={setSelectedCategory}>
          <SelectTrigger className="w-64">
            <SelectValue placeholder="Select category" />
          </SelectTrigger>
          <SelectContent>
            {categories.map((cat) => (
              <SelectItem key={cat} value={cat}>{cat}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <TemplateRadioGroup
        templates={filtered.map((t) => ({
          id: `DEFAULT::${t.name}`,
          name: t.name,
          description: t.description,
        }))}
        onChange={(id) => {
          const selectedTemplate = templates.find(
            (t) => `DEFAULT::${t.name}` === id
          )
          if (selectedTemplate) {
            onChange({
              id: null,
              name: selectedTemplate.name,
              agenda_usage: selectedTemplate.agenda_usage,
            })
          }
        }}
        value={`DEFAULT::${value.name}`}
        isLoading={isLoading}
      />
    </div>
  )
}

export const UserTemplateSelect = ({
  onChange,
  value,
}: {
  onChange: (template: Template) => void
  value: Template
}) => {
  const { data: templates = [], isLoading } = useQuery(
    getUserTemplatesUserTemplatesGetOptions()
  )
  if (!isLoading && !templates.length) {
    return (
      <p className="text-muted-foreground mb-4 flex items-center gap-1 text-sm">
        You haven&apos;t made any templates yet. Click the
        <FileText className="inline" size="1rem" /> button above to create and
        edit your templates.
      </p>
    )
  }
  return (
    <TemplateRadioGroup
      templates={templates.map((t) => ({
        id: t.id!,
        name: t.name,
        description: t.description || '',
      }))}
      onChange={(id) => {
        const selectedTemplate = templates.find((t) => t.id === id)
        if (selectedTemplate) {
          onChange({
            id: selectedTemplate.id!,
            name: selectedTemplate.name,
            agenda_usage: 'not_used',
          })
        }
      }}
      value={value.id!}
      isLoading={isLoading}
    />
  )
}
