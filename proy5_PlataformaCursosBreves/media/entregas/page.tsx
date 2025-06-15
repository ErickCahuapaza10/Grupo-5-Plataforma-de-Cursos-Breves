"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Edit, Link, User, ChevronDown } from "lucide-react"

interface Enrollment {
  id: number
  nombre: string
  gestion: string
  periodo: string
}

interface Subject {
  id: number
  sigla: string
  materia: string
  paralelo: string
}

interface Grade {
  id: number
  ponderacion: string
  nota: string
}

export default function StudentEnrollmentSystem() {
  const [showEnrollmentModal, setShowEnrollmentModal] = useState(false)
  const [showGradesModal, setShowGradesModal] = useState(false)
  const [selectedSubject, setSelectedSubject] = useState<Subject | null>(null)

  const enrollments: Enrollment[] = [
    { id: 1, nombre: "PRIMERO 2025", gestion: "2025", periodo: "PRIMERO" },
    { id: 2, nombre: "VERANO 2024", gestion: "2024", periodo: "VERANO" },
    { id: 3, nombre: "SEGUNDO 2024", gestion: "2024", periodo: "SEGUNDO" },
    { id: 4, nombre: "INVIERNO 2024", gestion: "2024", periodo: "INVIERNO" },
    { id: 5, nombre: "PRIMERO 2024", gestion: "2024", periodo: "PRIMERO" },
  ]

  const subjects: Subject[] = [
    { id: 1, sigla: "INF-121", materia: "PROGRAMACIÓN II", paralelo: "E" },
    { id: 2, sigla: "INF-134", materia: "ESTADÍSTICA II", paralelo: "B" },
    { id: 3, sigla: "TRA-136", materia: "METODOLOGIA DE LA INVESTIGACION", paralelo: "A" },
    { id: 4, sigla: "INF-133", materia: "PROGRAMACIÓN WEB III", paralelo: "B" },
    { id: 5, sigla: "SIS-254", materia: "METODOS NUMERICOS I", paralelo: "A" },
  ]

  const grades: Grade[] = [
    { id: 1, ponderacion: "1ER EXAMEN", nota: "11/25" },
    { id: 2, ponderacion: "2DO EXAMEN", nota: "14/25" },
    { id: 3, ponderacion: "EXAMEN FINAL", nota: "0/30" },
    { id: 4, ponderacion: "AYUD", nota: "0/10" },
    { id: 5, ponderacion: "OTROS", nota: "0/10" },
  ]

  const handleIngresar = (enrollment: Enrollment) => {
    if (enrollment.nombre === "PRIMERO 2025") {
      setShowEnrollmentModal(true)
    }
  }

  const handleEditSubject = (subject: Subject) => {
    setSelectedSubject(subject)
    setShowEnrollmentModal(false)
    setShowGradesModal(true)
  }

  const handleCloseGrades = () => {
    setShowGradesModal(false)
    setShowEnrollmentModal(true)
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-blue-800 text-white px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-8">
            <div className="text-xl font-bold">S.S.A.</div>
            <nav className="flex space-x-6">
              <div className="flex items-center space-x-1 cursor-pointer">
                <span>Mis Documentos</span>
                <ChevronDown className="w-4 h-4" />
              </div>
              <div className="flex items-center space-x-1 cursor-pointer">
                <span>Administración Personal</span>
                <ChevronDown className="w-4 h-4" />
              </div>
              <div className="flex items-center space-x-1 cursor-pointer">
                <span>Inscripciones</span>
                <ChevronDown className="w-4 h-4" />
              </div>
              <div className="flex items-center space-x-1 cursor-pointer">
                <span>Seguridad</span>
                <ChevronDown className="w-4 h-4" />
              </div>
            </nav>
          </div>
          <div className="flex items-center space-x-2">
            <User className="w-4 h-4" />
            <span>JOSE IGNACIO MAMANI RAMOS</span>
            <ChevronDown className="w-4 h-4" />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-6 py-8">
        {/* Info Card */}
        <Card className="mb-6 bg-blue-50 border-blue-200">
          <CardContent className="p-6">
            <h1 className="text-2xl font-semibold text-blue-800 mb-3">Administrar Mis Inscripciones</h1>
            <p className="text-blue-700">
              Gestiona <strong>inscripciones</strong> durante su <strong>formación académica</strong> a partir de la
              implementación del Sistema de Seguimiento Académico en su Carrera, para{" "}
              <strong>ver detalles de su inscripción</strong> presione sobre un registro de la lista desplegada.
            </p>
          </CardContent>
        </Card>

        {/* Enrollments Table */}
        <Card>
          <CardContent className="p-0">
            <Table>
              <TableHeader className="bg-green-100">
                <TableRow>
                  <TableHead className="font-semibold text-gray-800">Nro.</TableHead>
                  <TableHead className="font-semibold text-gray-800">Nombre</TableHead>
                  <TableHead className="font-semibold text-gray-800">Gestion</TableHead>
                  <TableHead className="font-semibold text-gray-800">Periodo</TableHead>
                  <TableHead className="font-semibold text-gray-800"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {enrollments.map((enrollment) => (
                  <TableRow key={enrollment.id} className="hover:bg-gray-50">
                    <TableCell>{enrollment.id}</TableCell>
                    <TableCell className="font-medium">{enrollment.nombre}</TableCell>
                    <TableCell>{enrollment.gestion}</TableCell>
                    <TableCell>{enrollment.periodo}</TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Button
                          size="sm"
                          className="bg-amber-700 hover:bg-amber-800 text-white"
                          onClick={() => handleIngresar(enrollment)}
                        >
                          Ingresar
                        </Button>
                        <Button size="sm" className="bg-orange-400 hover:bg-orange-500 text-white">
                          📅 Horarios
                        </Button>
                        {(enrollment.id === 2 || enrollment.id === 4) && (
                          <Button size="sm" className="bg-green-500 hover:bg-green-600 text-white">
                            📄 Obtener CP
                          </Button>
                        )}
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>

      {/* Enrollment Modal */}
      <Dialog open={showEnrollmentModal} onOpenChange={setShowEnrollmentModal}>
        <DialogContent className="max-w-5xl max-h-[90vh] overflow-y-auto">
          <DialogHeader className="bg-blue-600 text-white p-4 -m-6 mb-4">
            <DialogTitle className="text-xl">Realizar Inscripción</DialogTitle>
          </DialogHeader>

          {/* Warning Message */}
          <div className="bg-red-50 border border-red-200 p-3 rounded mb-4">
            <p className="text-red-700 text-sm">USTED ESTA FUERA DEL RANGO PERMITIDO DE INSCRIPCION</p>
          </div>

          {/* Student Info */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <p className="text-sm">
                <span className="text-red-600">🎓</span> <strong>Matricula Nro. 27720-2025</strong>
              </p>
              <p className="text-sm">
                📚 Max.Materias a Insc: <strong>6</strong>
              </p>
              <p className="text-sm">
                👤 Inscrito a <strong>5</strong> Materias.
              </p>
              <p className="text-sm text-red-600">
                <strong>FECHA :</strong> 17/02/2025 a 17/02/2025
              </p>
              <p className="text-sm text-blue-600">
                <strong>HORA :</strong> 18:30 a 19:30
              </p>
            </div>
            <div className="flex justify-end space-x-2">
              <Button className="bg-amber-700 hover:bg-amber-800 text-white">📄 Ver Horario</Button>
              <Button className="bg-orange-500 hover:bg-orange-600 text-white">📋 Generar Boleta</Button>
            </div>
          </div>

          {/* Subjects Table */}
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>#</TableHead>
                <TableHead>Sigla</TableHead>
                <TableHead>Materia</TableHead>
                <TableHead>Ver Paralelos</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {subjects.map((subject, index) => (
                <TableRow key={subject.id}>
                  <TableCell>{index + 1}</TableCell>
                  <TableCell>{subject.sigla}</TableCell>
                  <TableCell>{subject.materia}</TableCell>
                  <TableCell>
                    <div className="flex space-x-2">
                      <Button
                        size="sm"
                        className={`${
                          subject.paralelo === "E"
                            ? "bg-orange-400"
                            : subject.paralelo === "B"
                              ? "bg-green-400"
                              : "bg-yellow-400"
                        } hover:opacity-80 text-white`}
                      >
                        Par {subject.paralelo}
                      </Button>
                      <Button
                        size="sm"
                        className="bg-blue-600 hover:bg-blue-700 text-white"
                        onClick={() => handleEditSubject(subject)}
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button size="sm" className="bg-green-500 hover:bg-green-600 text-white">
                        <Link className="w-4 h-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </DialogContent>
      </Dialog>

      {/* Grades Modal */}
      <Dialog open={showGradesModal} onOpenChange={setShowGradesModal}>
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
          <DialogHeader className="bg-blue-600 text-white p-4 -m-6 mb-4">
            <DialogTitle className="text-xl">ESTADÍSTICA II</DialogTitle>
          </DialogHeader>

          {/* Grades Table */}
          <Table className="mb-6">
            <TableHeader>
              <TableRow>
                <TableHead>#</TableHead>
                <TableHead>Ponderacion</TableHead>
                <TableHead>Nota</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {grades.map((grade, index) => (
                <TableRow key={grade.id}>
                  <TableCell>{index + 1}</TableCell>
                  <TableCell>{grade.ponderacion}</TableCell>
                  <TableCell>{grade.nota}</TableCell>
                </TableRow>
              ))}
              <TableRow className="bg-green-100">
                <TableCell></TableCell>
                <TableCell className="font-bold">NOTA FINAL</TableCell>
                <TableCell className="font-bold">25/100</TableCell>
              </TableRow>
            </TableBody>
          </Table>

          {/* Teacher Info */}
          <div className="grid grid-cols-2 gap-8 mb-6">
            <div>
              <h3 className="font-semibold mb-2">INFORMACION DOC</h3>
              <p className="text-sm">Lic. BENITO OSCAR SINANI BELTRAN</p>
              <p className="text-sm font-semibold">LUNES - MIERCOLES</p>
              <p className="text-sm font-semibold">14:00 a 16:00 - PB-A1</p>
            </div>
            <div>
              <h3 className="font-semibold mb-2">INFORMACION AUX</h3>
              <div className="bg-yellow-50 p-3 rounded">{/* Placeholder for auxiliary information */}</div>
            </div>
          </div>

          {/* Close Button */}
          <div className="flex justify-end">
            <Button variant="outline" onClick={handleCloseGrades}>
              Cerrar
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}
